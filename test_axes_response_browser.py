"""Axis-following contact, skew, response paths and shared live views."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from test_operator_browser import configuration

def main():
 c=configuration();c['scan_zones']=[]
 c['scan_plan'].update(azimuth_start_deg=-180,azimuth_end_deg=180,z_start_mm=-350,z_end_mm=350)
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=browser.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(Path('nozzle_operator.html').read_text().replace('__CONFIG__',json.dumps(c)))
  assert page.evaluate('motionMode()')=='free'
  page.evaluate('az=-50;z=-100;heading=0;draw()')
  page.locator('#motionAxis').select_option('main')
  page.evaluate('moveOnSurface(-48,200)')
  assert abs(page.evaluate('z')+100)<1e-8
  page.locator('#motionAxis').select_option('nozzle')
  assert page.evaluate('orbitCurve().length')==144
  # Start on a safe orbit point, make a complete contour with the contact constraint.
  page.evaluate('const q=orbitCurve()[0];az=deg(Math.atan2(q[1],q[0]));z=q[2];heading=motionHeading(az,z);draw()')
  before=page.evaluate('[az,z,heading]')
  for _ in range(8):page.evaluate('stepOrbit(1)')
  after=page.evaluate('[az,z,heading]')
  assert abs(after[0]-before[0])+abs(after[1]-before[1])>1
  assert abs(after[2]-before[2])>1
  assert page.evaluate('footprintCheck(az,z).allowed')
  assert abs(page.evaluate('Math.hypot(...point(az,z).slice(0,2))')-200)<1e-8
  page.locator('#plus').click()
  assert abs(page.evaluate('Number(document.getElementById("headingTrim").value)')-1)<1e-8
  page.locator('#reset').click()
  assert page.evaluate('Number(document.getElementById("headingTrim").value)')==0
  assert abs(page.evaluate('heading-motionHeading(az,z)'))<1e-8
  page.evaluate('startRaster()');assert page.evaluate('timer') is None
  page.locator('#motionAxis').select_option('free')
  page.evaluate('az=-50;z=-100;heading=0;draw()')
  page.locator('#showResponse').check()
  result=page.evaluate('flawReturn()')
  assert result and result['event']['kind']=='flaw'
  assert result['event']['t']>0 and result['event']['amp']>0
  assert result['path'][-1]==page.evaluate('point(az,z)')
  assert result['model']=='ILLUSTRATIVE_RECIPROCAL_BACKSCATTER'
  page.locator('#rayView').select_option('3d')
  assert page.evaluate('window.BYTE_NDT.getScene().teaching_flaw_return.event.t')==result['event']['t']
  # Both projected views change the same physical contact pose.
  page.locator('#rayView').select_option('section')
  before_z=page.evaluate('z')
  page.evaluate("document.getElementById('section').dispatchEvent(new WheelEvent('wheel',{deltaY:1,cancelable:true}))")
  page.wait_for_timeout(80)
  assert abs(page.evaluate('heading')-1)<1e-8
  page.evaluate('dragProjectedProbe(5,720)');page.wait_for_timeout(80)
  assert abs(page.evaluate('z')-before_z)>0.1
  page.evaluate('C.workflow="REAL_EXAM_PREPARATION";draw()')
  assert page.evaluate('flawReturn()') is None
  assert not errors,errors
  browser.close()
 print('Axis contour contact, main-axis lock, local skew, raster separation, reciprocal teaching return and examination suppression: OK')
if __name__=='__main__':main()
