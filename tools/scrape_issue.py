import re, sys, json, html, urllib.request
org_repo, n = sys.argv[1], sys.argv[2]
url = f'https://github.com/{org_repo}/issues/{n}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
s = urllib.request.urlopen(req, timeout=60).read().decode('utf8', 'replace')
m = re.search(r'<script type="application/json" data-target="react-app.embeddedData">(.*?)</script>', s, re.S)
if not m:
    print('NO EMBEDDED DATA'); sys.exit(1)
d = json.loads(html.unescape(m.group(1)))
issue = d['payload']['issueViewerRoute']['data']['repository']['issue']
print(f"# {url}")
print(f"TITLE: {issue.get('title')}")
print(f"STATE: {issue.get('state')}  opened {issue.get('createdAt','')[:10]} by {(issue.get('author') or {}).get('login')}  labels={[l['name'] for l in issue.get('labels',{}).get('edges',[]) and [e['node'] for e in issue['labels']['edges']]] if isinstance(issue.get('labels'),dict) else ''}")
print(f"\n--- opening post by {(issue.get('author') or {}).get('login')} on {issue.get('createdAt','')[:10]}:\n{issue.get('body','')}")
seen = set()
items = issue.get('frontTimelineItems', {}).get('edges', []) + issue.get('timelineItems', {}).get('edges', []) + issue.get('backTimelineItems', {}).get('edges', [])
for e in items:
    node = e.get('node') or {}
    t = node.get('__typename')
    if t == 'IssueComment':
        key = node.get('id')
        if key in seen: continue
        seen.add(key)
        print(f"\n--- comment by {(node.get('author') or {}).get('login')} on {node.get('createdAt','')[:10]}:\n{node.get('body','')}")
    elif t in ('ClosedEvent', 'ReopenedEvent', 'CrossReferencedEvent', 'ReferencedEvent', 'LabeledEvent', 'RenamedTitleEvent', 'ConnectedEvent'):
        extra = ''
        src = node.get('source') or node.get('commit') or {}
        if isinstance(src, dict):
            extra = src.get('url') or src.get('title') or src.get('abbreviatedOid') or ''
            if src.get('number'): extra = f"#{src['number']} {src.get('title','')} ({src.get('__typename','')}) {src.get('url','')}"
        print(f"\n[{t} {node.get('createdAt','')[:10]} {extra}]")
total = issue.get('timelineItems', {}).get('totalCount')
print(f"\n(total timeline items: {total}; comments shown: {len(seen)})")
