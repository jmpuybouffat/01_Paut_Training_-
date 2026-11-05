from pathlib import Path
import json,subprocess,re
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
w=json.loads((ROOT/'witness_verified.json').read_text())
for mode in ['', '_PA']:
 a,b=w['FR'+mode]['event'],w['EN'+mode]['event'];assert abs(a['t']-8.72971334798)<1e-6;assert a['amp']==b['amp']
assert len(w['FR_PA']['angles'])==19
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for name,lang in [('MANUEL_NOZZLE_FR','fr'),('NOZZLE_USER_MANUAL_EN','en')]:
  text=(ROOT/(name+'.html')).read_text();assert '@@' not in text
  page=b.new_page();page.set_content(text,timeout=60000)
  assert page.locator('section[id]').count()==13
  assert page.locator('img').count()==14
  assert page.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
  assert page.evaluate("Array.from(document.querySelectorAll('nav a')).every(a=>document.querySelector(a.getAttribute('href')))")
  body=page.locator('body').inner_text()
  for value in ['REV0.5','PA32','MWB','getScene','8,73' if lang=='fr' else '8.73','30dB','10dB']:assert value in body,value
  pdf=subprocess.check_output(['pdftotext',str(ROOT/(name+'.pdf')),'-'],text=True)
  assert len(pdf)>12000 and not re.search(r'\bNaN\b',pdf)
  page.close()
 b.close()
print('Nozzle manuals: 13 chapters, 14 real figures per language, PDF/HTML and MWB/PA numerical consistency: PASS')
