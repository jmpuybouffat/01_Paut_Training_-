"""Geometric stop checks for manual and raster motion in Chromium."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from test_operator_browser import configuration


def main():
 c=configuration();c['scan_zones']=[]
 c['scan_plan'].update(azimuth_start_deg=-60,azimuth_end_deg=60,z_start_mm=-400,z_end_mm=400,margin_mm=2)
 c['mwb'].update(body_length_mm=24,body_width_mm=14)
 template=Path(__file__).with_name('nozzle_operator.html').read_text()
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=browser.new_page(viewport=dict(width=1400,height=1200));errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(template.replace('__CONFIG__',json.dumps(c)))
  assert page.evaluate('footprintCheck(-50,-395).reason')=='PIPE_END'
  assert page.evaluate('footprintCheck(0,100).reason')=='NOZZLE_OR_WELD'
  page.evaluate('C.scan_zones=[{assessment:"INACCESSIBLE",azimuth_start_deg:-51,azimuth_end_deg:-49,z_start_mm:-99.1,z_end_mm:-98.9}]')
  assert page.evaluate('footprintCheck(-50,-110).reason')=='EXCLUDED_ZONE','Thin excluded zone missed between footprint samples'
  page.evaluate('C.scan_zones=[];az=0;z=-100;heading=0;draw()')
  assert page.evaluate('advanceProbe(0,200)') is False
  assert page.evaluate('z')<50
  assert page.evaluate('footprintCheck(az,z).allowed') is True
  assert page.evaluate('motionEvents[motionEvents.length-1].reason')=='NOZZLE_OR_WELD'
  page.locator('#operatorSurface').select_option('unwrapped')
  page.evaluate('az=0;z=-100;heading=0;draw()')
  p=page.evaluate('map(az,z)');q=page.evaluate('map(0,200)');box=page.locator('#top').bounding_box()
  page.mouse.move(box['x']+p[0]/720*box['width'],box['y']+p[1]/430*box['height']);page.mouse.down()
  page.mouse.move(box['x']+q[0]/720*box['width'],box['y']+q[1]/430*box['height'],steps=12);page.mouse.up()
  assert page.evaluate('z')<50 and page.evaluate('drag') is False
  page.evaluate('az=0;z=-100;heading=0;lastPlanIndex=null;playDirection=1;C.scan_plan.points=[{azimuth_deg:0,z_mm:-100},{azimuth_deg:0,z_mm:200}];startRaster()')
  page.wait_for_timeout(400)
  assert page.evaluate('timer') is None and page.evaluate('lastPlanIndex')==0
  assert page.evaluate('z')<50
  page.locator('#reverseScan').click();page.locator('#demo').click();page.wait_for_timeout(300)
  assert abs(page.evaluate('z')+100)<1e-8,'Reverse failed to return from a partial blocked leg'
  page.evaluate('az=0;z=-100;playDirection=1;lastPlanIndex=null;startRaster()');page.locator('#pause').focus();page.keyboard.press('Escape')
  assert page.evaluate('timer') is None
  assert page.evaluate('motionEvents[motionEvents.length-1].reason')=='USER_STOP'
  width1=page.evaluate('stableSectionBounds().hi-stableSectionBounds().lo')
  page.evaluate('z=150')
  width2=page.evaluate('stableSectionBounds().hi-stableSectionBounds().lo')
  assert abs(width1-width2)<1e-8
  assert not errors,errors
  browser.close()
 print('Manual/raster footprint limits, thin excluded region, pipe end, nozzle, Escape and stable mono view: OK')

if __name__=='__main__':main()
