"""Optional Chromium interaction checks: run with system Python + Playwright."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from scan import plan_scan
from libraries import PROJECT_INDICATIONS


def configuration():
    zone=dict(zone='Demo',access='TO_ASSESS',assessment='FOOTPRINT_FITS_ONLY',available_length_mm=500,available_width_mm=500,probe_length_mm=20,probe_width_mm=15,travel_mm=20,margin_mm=2,azimuth_start_deg=-60,azimuth_end_deg=-20,z_start_mm=-200,z_end_mm=100)
    geometry=dict(main_OD_mm=400,main_thickness_mm=20,main_length_mm=800,nozzle_OD_mm=160,nozzle_thickness_mm=12,nozzle_length_mm=320,offset_mm=0,axis_angle_deg=63)
    indications=[dict(d,enabled=True,azimuth_deg=None,z_mm=None,depth_mm=None,orientation_deg=None) for d in PROJECT_INDICATIONS]
    indications[0].update(azimuth_deg=-50,z_mm=-90,depth_mm=10,orientation_deg=0)
    return dict(language='FR',workflow='TRAINING',geometry=geometry,joint=dict(gap_mm=2,land_mm=2,bevel_deg=35),material=dict(VT_m_s=3240),mwb=dict(refracted_angle_deg=45,frequency_MHz=2),scan_zones=[zone],indications=indications,scan_plan=dict(azimuth_start_deg=-50,azimuth_end_deg=-30,z_start_mm=-100,z_end_mm=0,beam_heading_deg=0,points=plan_scan(200,800,-50,-30,-100,0,10,[zone])))


def main():
    template=Path(__file__).with_name('nozzle_operator.html').read_text()
    config=configuration()
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        page=browser.new_page(viewport=dict(width=1400,height=1200));errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(template.replace('__CONFIG__',json.dumps(config)))
        assert page.evaluate('status(az,z)')=='PLANNED'
        assert page.evaluate('rayTrace().length')>=2
        assert page.evaluate('echoes(rayTrace()).length')>=1
        assert page.evaluate('rayTrace().every(s=>Math.abs(Math.hypot(s.b[0],s.b[1])-(s.kind==="ID"?Ri:R))<1e-3)')
        box=page.locator('#top').bounding_box()
        x=box['x']+45/720*box['width'];y=box['y']+390/430*box['height']
        page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+30,y-30,steps=5);page.mouse.up()
        assert page.evaluate('trail.length')>=5
        before=page.evaluate('heading');page.mouse.wheel(0,100);page.wait_for_timeout(150)
        assert page.evaluate('heading')!=before
        page.locator('#plus').click();page.locator('#demo').click();page.wait_for_timeout(350);page.locator('#pause').click()
        assert page.evaluate('playIndex')>0 and page.evaluate('timer') is None
        page.locator('#instructor').check();page.locator('#record').click()
        assert page.evaluate('samples.length')==1
        with page.expect_download() as d: page.locator('#download').click()
        assert d.value.suggested_filename=='NOZZLE_MANUAL_SCAN.json'
        page.evaluate('C.scan_zones[0].assessment="INACCESSIBLE";draw()')
        assert page.evaluate('rayTrace().length')==0
        page.evaluate('C.scan_zones[0].assessment="FOOTPRINT_FITS_ONLY";C.workflow="REAL_EXAM_PREPARATION";draw()')
        assert page.evaluate('echoes(rayTrace()).length')==0
        page.evaluate('C.scan_zones=[];draw()')
        assert page.evaluate('status(az,z)')=='UNASSESSED'
        page.locator('#reset').click()
        box=page.locator('#top').bounding_box()
        cx=box['x']+45/720*box['width'];cy=box['y']+390/430*box['height']
        before=page.evaluate('[az,z]')
        page.mouse.move(cx+4,cy-3);page.mouse.down();page.mouse.move(cx+4,cy-3);page.mouse.up();page.wait_for_timeout(80)
        after=page.evaluate('[az,z]')
        assert abs(after[0]-before[0])<1e-6 and abs(after[1]-before[1])<1e-6,'Probe jumped at grab'
        page.mouse.move(cx,cy);page.mouse.down();page.mouse.move(box['x']+box['width']+40,cy,steps=10);page.mouse.up()
        assert page.evaluate('drag') is False,'Pointer release lost outside canvas'
        timing=page.evaluate('''()=>{const t=performance.now();for(let i=0;i<30;i++){heading=i;draw()}return (performance.now()-t)/30}''')
        print(f'Mean redraw: {timing:.1f} ms; no grab jump; release outside canvas: OK')
        assert not errors,errors
        page.locator('#rayView').select_option('3d')
        camera=page.locator('#section').bounding_box()
        cx=camera['x']+camera['width']/2;cy=camera['y']+camera['height']/2
        old=page.evaluate('[cameraYaw,cameraPitch]')
        page.mouse.move(cx,cy);page.mouse.down();page.mouse.move(cx+40,cy+20,steps=5);page.mouse.up();page.wait_for_timeout(80)
        assert page.evaluate('[cameraYaw,cameraPitch]')!=old
        zoom=page.evaluate('cameraZoom');page.mouse.wheel(0,-100);page.wait_for_timeout(80)
        assert page.evaluate('cameraZoom')>zoom
        page.locator('#cameraReset').click();assert page.evaluate('cameraZoom')==1
        assert not errors,errors
        print('Synchronized nozzle 3D camera: drag, zoom and reset OK')
        page.screenshot(path='/workspace/nozzle_operator_check.png',full_page=True)
        browser.close()
    print('Nozzle browser: cylindrical rays, five-indication registry, drag, wheel, raster, pause, sample, export, exclusions, examination mode: OK')

if __name__=='__main__':main()
