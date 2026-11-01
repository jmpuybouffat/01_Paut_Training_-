import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from pathlib import Path
from test_operator_browser import configuration
from scan import plan_scan
from playwright.sync_api import sync_playwright
c=configuration();c['indications']=[];c['scan_zones']=[];c['joint']['reinforcement_mm']=3
c['scan_plan']=dict(azimuth_start_deg=-30,azimuth_end_deg=30,z_start_mm=-150,z_end_mm=150,beam_heading_deg=0,points=plan_scan(200,800,-30,30,-150,150,10,[]))
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(Path(__file__).with_name('nozzle_operator.html').read_text().replace('__CONFIG__',json.dumps(c)))
 result=page.evaluate('''()=>{const found={};for(const p of C.scan_plan.points){az=p.azimuth_deg;z=p.z_mm;rayCache=new Map();for(const e of geometryBackscatterEchoes(rayTrace())){if(!found[e.id]||e.amp>found[e.id].amp)found[e.id]={amp:e.amp,t:e.t,leg:e.leg,az,z}}}return found}''')
 print('Geometry scans:',result)
 assert 'GEOMETRY_root' in result and 'GEOMETRY_cap' in result,result
 page.evaluate('az=-50;z=-150;heading=0;C.mwb.refracted_angle_deg=45;rayCache=new Map()')
 assert page.evaluate('specularReceptionEchoes(rayTrace()).length')==0,'Angled wall bounce created artificial pulse'
 page.evaluate('C.mwb.refracted_angle_deg=0;rayCache=new Map()')
 echoes=page.evaluate('specularReceptionEchoes(rayTrace())')
 assert echoes and abs(echoes[0]['t']-40/3.24)<1e-4,echoes  # tolerance includes 0.0001 mm reflection-origin nudges
 page.evaluate('C.workflow="REAL_EXAM_PREPARATION";rayCache=new Map()')
 assert page.evaluate('allEchoes(rayTrace()).length')==0
 assert not errors,errors
 print('No automatic angled wall pulse; normal-incidence round trip; no synthetic examination events: OK')
 b.close()
