"""Prepare wiki routes; publish only after GitHub's first Home page exists."""
import argparse
from pathlib import Path
import re
import subprocess

REPO = 'https://github.com/Nvb-flipped/bayesian-handwritten-digit-recognition'
WIKI_GIT = REPO + '.wiki.git'


def prepare(root, destination):
    destination.mkdir(parents=True, exist_ok=True)
    pages = sorted((root/'docs/wiki').glob('*.md'))
    assert len(pages) == 6
    for page in pages:
        def route(match):
            target = match[1]
            if '://' in target or target.startswith('#'):
                return match[0]
            path = (page.parent/target).resolve()
            if not path.is_file():
                raise ValueError(f'Broken source link: {page.name}: {target}')
            if path.parent == page.parent and path.suffix == '.md':
                return ']('+REPO+'/wiki/'+path.stem+')'
            return ']('+REPO+'/blob/main/'+path.relative_to(root).as_posix()+')'
        text = re.sub(r'\]\(([^)]+)\)', route, page.read_text(encoding='utf8'))
        (destination/page.name).write_text(text, encoding='utf8', newline='\n')
    return pages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish', action='store_true', help='Clone and push the initialized wiki')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    ready = root/'tmp/wiki-ready'
    pages = prepare(root, ready)
    print(f'Prepared {len(pages)} wiki pages in {ready}.')
    if not args.publish:
        return
    remote = subprocess.run(['git', 'ls-remote', WIKI_GIT], capture_output=True, text=True)
    if remote.returncode or not remote.stdout.strip():
        raise SystemExit('Wiki is not initialized or accessible. Create Home through GitHub Wiki first; nothing was pushed.')
    clone = root/'tmp/wiki-publish'
    if not clone.exists():
        subprocess.run(['git', 'clone', WIKI_GIT, str(clone)], check=True)
    origin = subprocess.check_output(['git', '-C', str(clone), 'remote', 'get-url', 'origin'], text=True).strip()
    if origin != WIKI_GIT:
        raise SystemExit('Unexpected wiki remote; refusing publication.')
    subprocess.run(['git', '-C', str(clone), 'pull', '--ff-only'], check=True)
    for page in pages:
        (clone/page.name).write_bytes((ready/page.name).read_bytes())
    subprocess.run(['git', '-C', str(clone), 'add', '--', *[p.name for p in pages]], check=True)
    changed = subprocess.run(['git', '-C', str(clone), 'diff', '--cached', '--quiet']).returncode
    if changed:
        subprocess.run(['git', '-C', str(clone), 'commit', '-m', 'Publish verified method, protocol, results and AI workflow'], check=True)
        subprocess.run(['git', '-C', str(clone), 'push'], check=True)
    print('Wiki Git synchronization completed; verify public Home and content pages before claiming publication.')


if __name__ == '__main__':
    main()
