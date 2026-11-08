#!/usr/bin/env python3
"""Check generated drift, local links, fragment IDs and source dataset."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import subprocess, sys, json
ROOT=Path(__file__).resolve().parents[1]
before={p:p.read_bytes() for p in ROOT.glob('*.html')}
data=(ROOT/'data/schools.json').read_bytes()
subprocess.run([sys.executable,str(ROOT/'scripts/build.py')],check=True)
assert before=={p:p.read_bytes() for p in ROOT.glob('*.html')}, 'Generated pages differ: run scripts/build.py and commit outputs'
assert data==(ROOT/'data/schools.json').read_bytes(), 'Generated data differs'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set();self.h1=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  for key in ('href','src'):
   if a.get(key):self.links.append(a[key])
pages={}
for p in ROOT.glob('*.html'):
 parser=Page();parser.feed(p.read_text());pages[p]=parser
 assert parser.h1==1,f'{p.name}: expected one h1'
count=0
for p,parser in pages.items():
 for url in parser.links:
  u=urlsplit(url)
  if u.scheme or u.netloc:continue
  assert not u.path.startswith('/'),f'Absolute asset path breaks Pages: {url}'
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  assert target.exists(),f'{p.name}: missing {url}'
  if u.fragment and target in pages:assert u.fragment in pages[target].ids,f'Missing fragment {url}'
  count+=1
schools=json.loads((ROOT/'data/schools.json').read_text())['schools']
assert all(sum(s['grades'])==s['students'] for s in schools)
assert all(s['chineseStudents'] is None and s['highSchoolProgressionRate'] is None for s in schools)
print(f'PASS: {len(pages)} pages, {count} local references, generated drift and dataset totals.')
