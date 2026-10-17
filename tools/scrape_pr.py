import re, sys, html, urllib.request
from html.parser import HTMLParser

class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.out=[]
    def handle_starttag(self, tag, attrs):
        if tag in ('br','p','div','li','tr','pre','h1','h2','h3','h4','blockquote'): self.out.append('\n')
    def handle_endtag(self, tag):
        if tag in ('p','div','li','tr','pre','h1','h2','h3','h4','blockquote'): self.out.append('\n')
    def handle_data(self, d): self.out.append(d)
def totext(h):
    t=Text(); t.feed(h); s=''.join(t.out)
    return re.sub(r'\n{3,}', '\n\n', s).strip()

org_repo, n = sys.argv[1], sys.argv[2]
kind = sys.argv[3] if len(sys.argv) > 3 else 'pull'
url = f'https://github.com/{org_repo}/{kind}/{n}'
req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
s = urllib.request.urlopen(req, timeout=60).read().decode('utf8','replace')
print(f'# {url}')
title = re.search(r'<bdi class="js-issue-title[^"]*">(.*?)</bdi>', s, re.S)
print('TITLE:', totext(title.group(1)) if title else '?')
state = re.search(r'<span[^>]*class="State[^"]*"[^>]*>\s*(?:<svg.*?</svg>)?\s*([A-Za-z ]+?)\s*</span>', s, re.S)
print('STATE:', state.group(1).strip() if state else '?')
# comment bodies with preceding author and time
pos = 0
pat = re.compile(r'class="[^"]*js-comment-body[^"]*"[^>]*>', re.S)
for m in pat.finditer(s):
    start = m.end()
    end = s.find('</td>', start)
    if end == -1: end = s.find('</div>', start)
    body = s[start:end]
    before = s[max(0, m.start()-20000):m.start()]
    authors = re.findall(r'class="[^"]*\bauthor\b[^"]*"[^>]*>\s*([^<\s][^<]*?)\s*<', before)
    times = re.findall(r'<relative-time[^>]*datetime="([^"]+)"', before)
    kind = 'review-comment' if 'review-comment' in before[-3000:] or 'inline-comment' in before[-3000:] else 'comment'
    a = authors[-1] if authors else '?'
    t = times[-1][:10] if times else '?'
    txt = totext(body)
    txt = re.sub(r'\n\s*Sorry, something went wrong\.(.|\n)*?Please reload this page\.?', '', txt).strip()
    print(f'\n--- {kind} by {a} on {t}:\n{txt}')
# file paths of inline review threads
paths = re.findall(r'data-path="([^"]+)"', s)
if paths:
    print('\nREVIEW THREAD PATHS:', sorted(set(paths)))
