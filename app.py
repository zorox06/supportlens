from hashlib import sha256
import json
from pathlib import Path

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

import config
from src.agent import SupportAgent
from src.knowledge import SupportKnowledge,load_document
from src.tools import repository_name
from src.ui import setup_page,error_message

ROOT=Path(__file__).resolve().parent
setup_page()
st.markdown('<div class="eyebrow">SUPPORT THAT CAN SHOW ITS EVIDENCE</div>',unsafe_allow_html=True)
st.title('A problem in. A documented solution out.')
st.markdown('<p class="subtitle">Upload product documentation. SupportLens retrieves relevant passages, '
            'checks whether they support a fix, and uses Gemini to explain the next steps with citations.</p>',unsafe_allow_html=True)
with st.sidebar:
    st.header('SupportLens')
    key=st.text_input('Gemini API key',value=config.GEMINI_API_KEY,type='password')
    model=st.text_input('Gemini model ID',value=config.GEMINI_MODEL)
    embedding_model=st.text_input('Embedding model ID',value=config.EMBEDDING_MODEL)
    st.divider()
    repo=st.text_input('Product GitHub repository (optional)',placeholder='owner/repo')
    token=st.text_input('GitHub token (optional)',value=config.GITHUB_TOKEN,type='password')
    st.caption('The optional API lookup searches known issues for the selected product repository.')
    st.caption('Document chunks are sent to Gemini for embeddings; retrieved passages and recent messages are sent for responses.')
    if st.button('Reset session',key='reset'):
        if st.session_state.get('knowledge'):
            st.session_state['knowledge'].close()
        for name in ['knowledge','index_fingerprint','result','history','indexed_docs']:
            st.session_state.pop(name,None)
        st.rerun()

left,right=st.columns([1,1.65],gap='large')
with left:
    with st.container(border=True):
        st.subheader('01 / Build your knowledge base')
        samples=st.checkbox('Include DeskSync sample manuals',value=True)
        st.caption('DeskSync is a fictional sample product. Replace its manuals with your own to support a real product.')
        uploads=st.file_uploader('Product documents',type=['pdf','docx','md','txt'],accept_multiple_files=True)
        docs=[]; invalid=False
        if samples:
            for path in sorted((ROOT/'data').glob('*.md')):
                docs.extend(load_document(path.name,path.read_bytes()))
        for upload in uploads:
            try:
                docs.extend(load_document(upload.name,upload.getvalue()))
            except Exception as exc:
                st.error(f'{upload.name}: {error_message(exc)}'); invalid=True
        st.caption('10 MB per file; up to 100 PDF pages; scanned PDFs need OCR.')
        for source in sorted({d.metadata['source'] for d in docs}):
            st.write('📄 '+source)
        fingerprint=sha256(json.dumps([embedding_model,key,[(d.page_content,d.metadata) for d in docs]],sort_keys=True).encode()).hexdigest()
        indexed=st.session_state.get('index_fingerprint')==fingerprint
        if st.button('Index with Gemini embeddings',type='primary',width='stretch',key='index'):
            if not key or key=='PASTE_YOUR_GEMINI_KEY_HERE':
                st.error('Configure the Gemini key in local_config.py or enter it in the sidebar.')
            elif not docs or invalid:
                st.error('Add readable documents and resolve file errors first.')
            else:
                try:
                    with st.spinner('Chunking documents and creating Gemini vectors in Chroma…'):
                        knowledge=SupportKnowledge(docs,key,embedding_model)
                        old=st.session_state.get('knowledge')
                        if old:
                            old.close()
                        st.session_state['knowledge']=knowledge
                        st.session_state['index_fingerprint']=fingerprint
                        st.session_state['indexed_docs']=len(docs)
                        st.session_state['history']=[]
                        st.session_state.pop('result',None)
                        indexed=True
                except Exception as exc:
                    st.error(error_message(exc))
        if indexed:
            st.success(f"Ready · {len(st.session_state['knowledge'].chunks)} indexed chunks")
        else:
            st.info('Index the current documents before asking a question.')

with right:
    with st.container(border=True):
        st.subheader('02 / Describe the problem')
        examples=['DeskSync shows E104 and files are not syncing. What should I do?',
                  'My DeskSync account is locked. Can support unlock it?',
                  'My DeskSync workspace is paused. How do I resume syncing?',
                  'My printer has a paper jam. How do I fix it?']
        for i,example in enumerate(examples):
            if st.button(example,key=f'example_{i}',width='stretch'):
                st.session_state['question']=example
        question=st.text_area('Support request',value=examples[0],key='question',height=120,max_chars=4000)
        if st.button('Find a documented solution',type='primary',width='stretch',key='run'):
            if not indexed:
                st.error('Index the current documents with Gemini first.')
            elif not key:
                st.error('Provide your Gemini key.')
            else:
                try:
                    repository=repository_name(repo) if repo.strip() else ''
                    with st.status('Retrieving evidence and running the support graph…',expanded=True) as progress:
                        st.write('Gemini classifies the problem, searches Chroma, and assesses whether the passages support a fix.')
                        agent=SupportAgent(st.session_state['knowledge'],key,model,repository,token)
                        result=agent.run(question,st.session_state.get('history',[]))
                        result.update(model=model,embedding_model=embedding_model)
                        st.session_state['result']=result
                        st.session_state['history']=[*st.session_state.get('history',[]),HumanMessage(content=question),
                                                     AIMessage(content=result['answer'])][-6:]
                        progress.update(label='Support response ready',state='complete',expanded=False)
                except Exception as exc:
                    st.error(error_message(exc)); st.session_state.pop('result',None)
    result=st.session_state.get('result')
    if result:
        a,b,c=st.columns(3)
        a.metric('Retrieved passages',len(result['sources']))
        b.metric('Retrieval retries',result['retries'])
        c.metric('Citation IDs','Passed' if result['checks']['passed'] else 'Review')
        tabs=st.tabs(['Solution','Evidence','Agent trace','Ticket & export'])
        with tabs[0]:
            if not result['assessment']['sufficient']:
                st.warning('The documents did not establish a supported solution. Clarification or escalation is needed.')
            if not result['checks']['passed']:
                st.warning('Some citations need review after one correction. Check the retrieved passages.')
            st.markdown(result['answer'])
        with tabs[1]:
            for source in result['sources']:
                page=f" · page {source['page']}" if 'page' in source else ''
                with st.expander(f"[{source['id']}] {source['source']}{page} · chunk {source['chunk']}"):
                    st.caption(f"Cosine similarity: {source['similarity']} (not a confidence probability)")
                    st.text(source['text'])
            st.subheader('Evidence assessment')
            st.json(result['assessment'])
            if result.get('issues'):
                st.subheader('Known-issue API result'); st.json(result['issues'])
        with tabs[2]:
            st.caption('Executed graph steps, LLM usage where available, retrieval and tool results.')
            for i,event in enumerate(result['trace'],1):
                with st.expander(f"{i:02d} · {event['node']} · {event.get('tool',event.get('detail',''))}"):
                    st.json(event)
            st.code(result['graph'],language='mermaid')
            st.json(result['checks'])
        with tabs[3]:
            ticket=result.get('ticket')
            if ticket:
                st.info('Draft only. No ticket has been sent to a support team or GitHub.')
                st.json(ticket)
                st.download_button('Download ticket draft',json.dumps(ticket,indent=2),'support-ticket.json',mime='application/json')
            st.download_button('Download response',result['answer'],'supportlens-answer.md',mime='text/markdown')
            export={k:v for k,v in result.items() if k!='messages'}
            st.download_button('Download RAG evidence and trace',json.dumps(export,indent=2),'supportlens-run.json',mime='application/json')
    else:
        st.info('Index your manuals and run a request to see a Gemini-generated answer with source evidence.')

st.divider()
st.caption('Gemini classify → semantic retrieval → evidence assessment → retry or grounded response → citation validation')
