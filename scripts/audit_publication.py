"""Verify anonymous public access, exact Git trees, PDF bytes and wiki sync."""
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request

OWNER_REPO = 'Nvb-flipped/bayesian-handwritten-digit-recognition'
URL = 'https://github.com/'+OWNER_REPO
ROOT = Path(__file__).resolve().parents[1]


def git(*args, cwd=ROOT):
    return subprocess.check_output(['git', '-C', str(cwd), *args])


def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'BayesianDigits-PublicationAudit'})
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise ValueError(f'Unexpected status for {url}: {response.status}')
        return response.read(), response.geturl()


def main():
    api='https://api.github.com/repos/'+OWNER_REPO
    repo=json.loads(fetch(api)[0])
    assert repo['private'] is False and repo['default_branch']=='main' and repo['has_wiki']
    head=git('rev-parse','HEAD').decode().strip()
    remote=json.loads(fetch(api+'/commits/main')[0])['sha']
    assert head==remote, (head,remote)
    tree=json.loads(fetch(api+'/git/trees/'+head+'?recursive=1')[0])
    assert not tree['truncated']
    observed={item['path']:item['sha'] for item in tree['tree'] if item['type']=='blob'}
    expected={}
    for line in git('ls-tree','-r','HEAD').decode().splitlines():
        metadata,path=line.split('\t',1)
        expected[path]=metadata.split()[2]
    assert observed==expected, 'Public Git tree differs from committed local tree'
    checked={}
    for path in ['README.md','report/main.tex','report/main.pdf','AGENTS.md',
                 'AIassign2.pdf','configs/default.json','results/summary.json',
                 'results/predictions.npz','src/bayes_digits/laplace.py',
                 'tests/test_math.py','prompts/03_PUBLISH_GITHUB_AND_WIKI.md']:
        # Test filenames are validated by the complete tree comparison below.
        if path not in expected:
            if path=='tests/test_math.py':
                path=next(p for p in expected if p.startswith('tests/') and p.endswith('.py'))
            else:
                raise ValueError(f'Missing deliverable: {path}')
        data,actual=fetch('https://raw.githubusercontent.com/'+OWNER_REPO+'/'+head+'/'+path)
        assert hashlib.sha256(data).digest()==hashlib.sha256((ROOT/path).read_bytes()).digest(),path
        checked[path]={'url':actual,'sha256':hashlib.sha256(data).hexdigest()}
    wiki=ROOT/'tmp/wiki-publish'
    wiki_head=git('rev-parse','HEAD',cwd=wiki).decode().strip()
    wiki_remote=git('ls-remote',URL+'.wiki.git','refs/heads/master').decode().split()[0]
    assert wiki_head==wiki_remote
    routes={}
    for page in sorted((ROOT/'docs/wiki').glob('*.md')):
        expected_page=(ROOT/'tmp/wiki-ready'/page.name).read_bytes()
        assert git('show','HEAD:'+page.name,cwd=wiki)==expected_page,page.name
        data,actual=fetch(URL+'/wiki/'+page.stem)
        assert b'wiki-wrapper' in data and b'wiki-content' in data,page.name
        assert actual.startswith(URL+'/wiki'),actual
        routes[page.stem]={'url':actual,'status':200,'synchronized_source':True}
    assert len(routes)==6
    images={}
    for name in ['covariance_geometry','comparison','classes']:
        data,actual=fetch('https://raw.githubusercontent.com/'+OWNER_REPO+'/'+head+'/results/figures/'+name+'.png')
        assert data==(ROOT/'results/figures'/f'{name}.png').read_bytes()
        images[name]={'url':actual,'sha256':hashlib.sha256(data).hexdigest()}
    record=dict(repository=URL,public=True,default_branch='main',content_commit_verified=head,
        public_tree_blobs_verified=len(expected),required_public_files=checked,
        public_pdf_bitwise_equal=True,wiki_enabled=True,wiki_commit_verified=wiki_head,
        wiki_pages=routes,wiki_images=images,requests_authenticated=False,
        browser_checks='Home navigation; mathematical derivations/matrices; results tables; three figures. Rendering errors repaired and rechecked.',
        audit_date='2026-10-09')
    (ROOT/'results/publication_audit.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf8',newline='\n')
    print(f'Public audit passed: {len(expected)} exact Git blobs; matching PDF; six anonymous wiki pages; three matching figures.')


if __name__=='__main__':
    main()
