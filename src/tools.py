import re
from urllib.parse import urlparse

import httpx
from langchain_core.tools import tool


def repository_name(value: str) -> str:
    value = value.strip().rstrip('/')
    if value.startswith(('http://','https://')):
        url = urlparse(value)
        if url.scheme != 'https' or url.netloc != 'github.com' or url.query or url.fragment:
            raise ValueError('Use a GitHub owner/repo or HTTPS repository URL.')
        value = url.path.strip('/')
    if not re.fullmatch(r'[A-Za-z0-9_.-]{1,100}/[A-Za-z0-9_.-]{1,100}',value):
        raise ValueError('Use an owner/repo identifier.')
    if any(part in {'.','..'} for part in value.split('/')):
        raise ValueError('Invalid repository identifier.')
    return value


def known_issues(repo: str, query: str, token: str = '') -> dict:
    repo = repository_name(repo)
    headers = {'Accept':'application/vnd.github+json','User-Agent':'SupportLens/1.0'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    # Strip GitHub search operators from user text so the selected repository stays fixed.
    words = re.findall(r'[A-Za-z0-9_-]+',query)[:12]
    search = ' '.join(words) + f' repo:{repo} is:issue'
    with httpx.Client(timeout=20,follow_redirects=False) as client:
        response = client.get('https://api.github.com/search/issues',
                              params={'q':search,'per_page':5},headers=headers)
    if response.status_code != 200:
        return {'repo':repo,'error':f'GitHub lookup returned HTTP {response.status_code}.','issues':[]}
    data = response.json()
    return {'repo':repo,'total_matches':data.get('total_count',0),
            'issues':[{'number':i['number'],'title':i['title'],'state':i['state'],
                       'url':i['html_url'],'excerpt':(i.get('body') or '')[:800]}
                      for i in data.get('items',[])],
            'note':'Matches are leads, not proof that the reported problem has the same cause.'}


def build_tools(kb, repository: str = '', token: str = ''):
    @tool
    def search_manuals(query: str, k: int = 5) -> list[dict]:
        """Retrieve semantically relevant passages from uploaded product documents with citation IDs."""
        return kb.search(query,k)

    @tool
    def lookup_known_issues(query: str) -> dict:
        """Search actual GitHub issues in the user-selected product repository for related software problems."""
        if not repository:
            return {'issues':[],'error':'No product repository selected. Do not invent issue matches.'}
        return known_issues(repository,query,token)

    @tool
    def draft_support_ticket(summary: str, category: str, attempted_steps: list[str],
                             missing_information: list[str]) -> dict:
        """Draft an exportable support ticket locally. This never sends or creates a GitHub issue."""
        return {'summary':summary[:500], 'category':category[:100],
                'attempted_steps':attempted_steps[:15], 'missing_information':missing_information[:15],
                'status':'draft', 'submitted':False}

    return [search_manuals,lookup_known_issues,draft_support_ticket]
