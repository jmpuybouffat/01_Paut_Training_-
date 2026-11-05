"""Actual Streamlit PA preset, language persistence and non-resetting PDF downloads."""
from pathlib import Path
import json,hashlib,subprocess,time,urllib.request,re
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
proc=subprocess.Popen(['/workspace/nozzle-venv/bin/python','-m','streamlit','run','app.py','--server.port','8516','--server.headless','true','--browser.gatherUsageStats','false'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
 for _ in range(120):
  try:urllib.request.urlopen('http://127.0.0.1:8516/_stcore/health',timeout=1);break
  except OSError:time.sleep(.2)
 with sync_playwright() as p:
  b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1500,'height':1100},accept_downloads=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto('http://127.0.0.1:8516',timeout=60000)
  page.get_by_role('tab').nth(2).click();page.get_by_role('button',name=re.compile('Charger le test témoin PA')).click()
  frame=page.get_by_role('tabpanel').first.locator('iframe').first.element_handle().content_frame();frame.wait_for_function("typeof C!=='undefined'&&C.acquisition==='PHASED_ARRAY_32'&&!scatteringState().pending&&scatteringState().pa?.sector.length===19",timeout=60000)
  assert frame.evaluate('C.pa.elements')==32;assert frame.evaluate('C.pa.pitch_mm')==.5
  frame.locator('#record').click();assert frame.evaluate('samples.length')==1
  page.get_by_role('tab').nth(3).click()
  for label,name in [('📘 Manuel Nozzle français · PDF','MANUEL_NOZZLE_FR.pdf'),('📗 Nozzle English user manual · PDF','NOZZLE_USER_MANUAL_EN.pdf')]:
   with page.expect_download() as d:page.get_by_role('button',name=label,exact=True).click()
   target=Path('/tmp')/name;d.value.save_as(target)
   assert hashlib.sha256(target.read_bytes()).digest()==hashlib.sha256((ROOT/'nozzle_documentation'/name).read_bytes()).digest()
   assert frame.evaluate('samples.length')==1
  page.get_by_role('radio',name=re.compile('English')).evaluate('(el)=>el.click()')
  page.get_by_role('tab').nth(2).click()
  # Native language rerun restores the local scan session and the PA method.
  deadline=time.monotonic()+60
  while time.monotonic()<deadline:
   try:
    english=page.get_by_role('tabpanel').first.locator('iframe').first.element_handle(timeout=1000).content_frame()
    english.wait_for_function("typeof C!=='undefined'&&C.language==='EN'&&C.acquisition==='PHASED_ARRAY_32'&&!scatteringState().pending&&scatteringState().pa?.sector.length===19",timeout=1000);break
   except Exception:page.wait_for_timeout(100)
  else:raise AssertionError('Language change did not preserve PA')
  assert english.locator('#paSectorTitle').inner_text().startswith('PA · Z / depth')
  assert english.evaluate('samples.length')==1,'Language change lost the saved scan session'
  assert english.evaluate('samples[0].gain_db')==30
  (ROOT/'nozzle_documentation/SCENE_TEMOIN_PA_NOZZLE.json').write_text(json.dumps(english.evaluate('window.BYTE_NDT.getScene()'),ensure_ascii=False,indent=2)+'\n')
  english.locator('#reportTitle').click()
  english.locator('#reportOperator').fill('Test')
  english.locator('#reportNotes').fill('Signal <check>')
  with page.expect_download() as d:english.locator('#reportExport').click()
  report=Path('/tmp/NOZZLE_REPORT_TEST.html');d.value.save_as(report)
  assert 'Signal &lt;check&gt;' in report.read_text()
  assert not errors,errors;b.close()
 print('Nozzle Streamlit: native PA preset, 19-beam sector, FR/EN persistence, PDF bytes and scan preserved on downloads: PASS')
finally:proc.terminate();proc.wait(timeout=15)
