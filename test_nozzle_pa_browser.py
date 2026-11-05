from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from test_operator_browser import configuration
c=configuration();c['scan_zones']=[];c['default_field_view']='scattered';c['acquisition']='PHASED_ARRAY_32';c['mwb'].update(frequency_MHz=5,refracted_angle_deg=45)
c['pa']=dict(elements=32,frequency_MHz=5,pitch_mm=.5,element_width_mm=.45,elevation_mm=12,focus_mm=30,sector_min_deg=35,sector_max_deg=70,angular_step_deg=2,selected_angle_deg=45,wedge_nominal_shear_deg=55)
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1450,'height':1100});errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.set_content(Path('nozzle_operator.html').read_text().replace('__CONFIG__',json.dumps(c)))
 def ready():
  page.wait_for_function('typeof scatteringState===\'function\'&&!scatteringState().pending',timeout=60000)
  assert page.evaluate('scatteringState().error||null') is None,page.locator('#scatterInfo').inner_text()
 ready();s=page.evaluate('scatteringState()');assert len(s['pa']['angles'])==19;assert s['pa']['angles'][0]==35 and s['pa']['angles'][-1]==70
 assert s['events'] and abs(s['events'][0]['t']-8.729713348)<1e-6
 assert s['selected']['received']['aperture_samples']>32
 assert s['cut']['cells'] and s['volume'] and s['pa']['incident']['cells']
 assert page.locator('#gain').input_value()=='30'
 assert page.locator('#gateThreshold').input_value()=='0.001'
 assert page.locator('#paSectorCard').is_visible();assert page.locator('#paBscanCard').is_visible()
 page.locator('#record').click();assert page.evaluate('samples[0].pa_sector.length')==19
 assert page.evaluate('window.BYTE_NDT.getScene().pa.sector.length')==19
 assert page.evaluate('window.BYTE_NDT.getScene().pa.incident_field.cells.length')>0
 baseline=s['events'][0]['amp'];page.locator('#paSelected').fill('65');page.locator('#paSelected').press('Tab');ready();changed=page.evaluate('scatteringState().events[0]?.amp||0');assert abs(changed-baseline)>baseline*.05,(baseline,changed)
 page.evaluate('C.workflow="REAL_EXAM_PREPARATION";draw()');ready();assert page.evaluate('scatteringState().events.length')==0
 assert page.evaluate('paProjectedEvents(scatteringState()).length')==0
 assert not errors,errors
 page.screenshot(path='/tmp/nozzle-pa-checked.png',full_page=True);b.close();print(f'Nozzle PA: sector, selected-ray coupled backscatter, S/B scan, recorded/exported sector, steering sensitivity and exam suppression: PASS ({baseline:.5g} → {changed:.5g})')
