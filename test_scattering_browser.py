"""Computed field, aperture reception, freshness and parameter sensitivity."""
import json
import html
from pathlib import Path
from playwright.sync_api import sync_playwright
from test_operator_browser import configuration

def main():
 c=configuration();c['scan_zones']=[];c['default_field_view']='scattered';c['mwb']['frequency_MHz']=4
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=browser.new_page(viewport=dict(width=1400,height=1200));errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(Path('nozzle_operator.html').read_text().replace('__CONFIG__',json.dumps(c)))
  def ready():
   page.wait_for_function('scatteringState().pending===false',timeout=60000)
   assert page.evaluate('scatteringState().error||null') is None,page.locator('#scatterInfo').inner_text()
  ready()
  s=page.evaluate('scatteringState()')
  assert s['selected']['surface']['shape']=='FINITE_PLANAR_RECTANGLE'
  assert s['selected']['prepared']['nodes'] and len(s['selected']['prepared']['nodes'])>100
  assert abs(s['selected']['total_area_mm2']-18)<1e-8
  event=s['events'][0];baseline=event['amp']
  assert 0<baseline<1 and abs(event['t']-8.729713348)<1e-6
  assert abs(event['amp']-s['selected']['received']['amplitude']/.05)<1e-12
  assert event['mechanism']==s['model'] and event['reflections_before_target']==0
  assert page.evaluate('allEchoes(rayTrace()).every(e=>e.mechanism===scatteringState().model)')
  dbs=[p['db'] for p in s['cut']['cells']]
  assert max(dbs)-min(dbs)>25 and len(s['volume'])>100
  assert page.locator('#showResponse').is_disabled()
  assert page.evaluate('window.BYTE_NDT.getScene().scalar_scattering.events[0].amp')==event['amp']
  page.locator('#record').click()
  assert page.evaluate('samples[0].signal_model')==s['model']
  assert abs(page.evaluate('samples[0].training_peak.amp')-baseline)<1e-12
  # Do not reuse a previously computed field while position/orientation changes.
  duration=page.evaluate('(()=>{const start=performance.now();heading=10;draw();heading=20;draw();return performance.now()-start})()')
  assert duration<250,f'Main gesture thread blocked for {duration} ms'
  assert page.evaluate('scatteringState().pending') is True
  assert page.evaluate('scatteringState().events.length')==0
  assert page.locator('#record').is_disabled()
  ready();assert page.evaluate('scatteringState().pose.heading_deg')==20
  altered=page.evaluate('scatteringState().targets[0].amp')
  assert altered<baseline/2
  assert page.evaluate('scatteringState().reference_amplitude')==.05
  # Real surface orientation and frequency modify the integrated field/echo.
  page.evaluate('heading=0;C.indications[0].normal_tilt_deg=80;draw()');ready()
  tilted=page.evaluate('scatteringState().targets[0].amp');assert tilted<baseline/2
  page.evaluate('C.indications[0].normal_tilt_deg=45;C.mwb.frequency_MHz=5;draw()');ready()
  assert abs(page.evaluate('scatteringState().targets[0].amp')-baseline)>baseline*.01
  page.locator('#rayView').select_option('3d');assert not errors,errors
  # Gate selects the envelope event, not a renormalized harmonic field.
  page.locator('#gateStart').fill('30');page.locator('#gateEnd').fill('40')
  assert page.evaluate('drawAscan(allEchoes(rayTrace()))') is None
  page.evaluate('C.indications[0].enabled=false;draw()');ready()
  assert page.evaluate('scatteringState().events.length')==0
  page.evaluate('C.workflow="REAL_EXAM_PREPARATION";draw()')
  assert page.evaluate('allEchoes(rayTrace()).length')==0
  assert page.evaluate('scatteredVolume().length')==0
  assert not errors,errors
  print(f'Computed scalar field: {len(dbs)} section cells, {len(s["volume"])} volume cells; witness {event["t"]:.2f} µs, {baseline:.4f} relative; worker main-thread response {duration:.1f} ms; coupling, orientation, frequency, freshness, gates and examination suppression: OK')
  # Streamlit hosts the dashboard in a sandboxed iframe: workers must work there too.
  content=Path('nozzle_operator.html').read_text().replace('__CONFIG__',json.dumps(c))
  page.set_content('<iframe sandbox="allow-scripts allow-same-origin" srcdoc="'+html.escape(content,quote=True)+'"></iframe>')
  frame=page.frames[1]
  frame.wait_for_function('typeof scatteringState!=="undefined" && scatteringState().pending===false',timeout=60000)
  assert frame.evaluate('scatteringState().events.length')>0
  assert frame.evaluate('scatteringState().error||null') is None
  frame.locator('#focusScatter').click()
  assert frame.evaluate('surfaceZoom')==2.4
  assert frame.evaluate('Math.hypot(...surfaceFocus)')>0
  assert not errors,errors
  print('Sandboxed Streamlit-style iframe: Blob worker and flaw-focus camera OK')
  browser.close()
if __name__=='__main__':main()
