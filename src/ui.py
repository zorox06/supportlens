import streamlit as st


def error_message(exc):
    text=str(exc).lower()
    if isinstance(exc,ValueError):
        return 'Check document format, readable text, upload limits, request length and repository identifier.'
    if '429' in text or 'quota' in text:
        return 'API quota or rate limit reached. Wait and retry.'
    if '503' in text or 'unavailable' in text:
        return 'Gemini is temporarily busy. Retry or select another available model ID.'
    if any(t in text for t in ['401','403','api_key_invalid','api key not valid']):
        return 'Authentication or API access was rejected. Check the configured key.'
    if '404' in text or 'not found' in text:
        return 'The requested model or repository is unavailable. Check the identifier.'
    if 'timeout' in text or 'timed out' in text:
        return 'The API request timed out. Check your connection and try again.'
    return 'The agent could not complete the request. Check the connection, credentials and model IDs.'


def setup_page():
    st.set_page_config(page_title='SupportLens · Agentic RAG',page_icon='◉',layout='wide')
    st.markdown('''<style>
    .block-container {max-width:1320px; padding-top:2.4rem;}
    .eyebrow {color:#70E1CE;font-size:.8rem;font-weight:700;letter-spacing:.14em;}
    .subtitle {color:#A5B4CF;font-size:1.05rem;line-height:1.65;max-width:780px;}
    [data-testid="stMetric"] {padding:1rem;background:#142033;border-radius:12px;}
    @media(max-width:800px) {
      [data-testid="stHorizontalBlock"] {flex-wrap:wrap;}
      [data-testid="stColumn"] {min-width:100% !important;width:100% !important;flex:1 1 100% !important;}
    }
    </style>''',unsafe_allow_html=True)
