"""Optional Chromium interaction checks: run with system Python + Playwright."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from scan import plan_scan
from libraries import PROJECT_INDICATIONS
from acoustic_field import scalar_aperture_cut
from joint_profiles import faceted_joint_profiles


def configuration():
    zone=dict(zone='Demo',access='TO_ASSESS',assessment='FOOTPRINT_FITS_ONLY',available_length_mm=500,available_width_mm=500,probe_length_mm=20,probe_width_mm=15,travel_mm=20,margin_mm=2,azimuth_start_deg=-60,azimuth_end_deg=-20,z_start_mm=-200,z_end_mm=100)
    geometry=dict(main_OD_mm=400,main_thickness_mm=20,main_length_mm=800,nozzle_OD_mm=160,nozzle_thickness_mm=12,nozzle_length_mm=320,offset_mm=0,axis_angle_deg=63)
    indications=[dict(d,enabled=True,azimuth_deg=None,z_mm=None,depth_mm=None,orientation_deg=None) for d in PROJECT_INDICATIONS]
    indications[0].update(azimuth_deg=-50,z_mm=-90,depth_mm=10,orientation_deg=0)
    return dict(joint_profiles=faceted_joint_profiles(200,180,80,63,0,800,2,2,35,3),direct_field=scalar_aperture_cut(2,3240,ns=60,nt=41,include_volume=True),language='FR',workflow='TRAINING',geometry=geometry,joint=dict(gap_mm=2,land_mm=2,bevel_deg=35),material=dict(VT_m_s=3240),mwb=dict(refracted_angle_deg=45,frequency_MHz=2),scan_zones=[zone],indications=indications,scan_plan=dict(azimuth_start_deg=-50,azimuth_end_deg=-30,z_start_mm=-100,z_end_mm=0,beam_heading_deg=0,points=plan_scan(200,800,-50,-30,-100,0,10,[zone])))


def main():
    template=Path(__file__).with_name('nozzle_operator.html').read_text()
    config=configuration()
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        page=browser.new_page(viewport=dict(width=1400,height=1200));errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(template.replace('__CONFIG__',json.dumps(config)))
        assert page.locator('#operatorSurface').input_value()=='3d'
        assert page.evaluate('C.joint_profiles.measured') is False
        assert page.evaluate('geometricReferences.root.length')>0
        assert not page.locator('#instructor').is_checked()
        assert page.locator('#showBeam').is_checked()
        assert page.evaluate('C.direct_field.model')=='HARMONIC_SCALAR_GREEN_RECTANGULAR_APERTURE'
        assert page.evaluate('Number.isFinite(fieldDb(10,0))')
        assert page.locator('#fieldView').input_value()=='teaching'
        page.locator('#fieldView').select_option('volume')
        assert page.evaluate('volumePoints().length')>0
        page.locator('#fieldView').select_option('cut')
        assert 'scalaire' in page.locator('#fieldScope').inner_text()
        page.locator('#fieldView').select_option('teaching')
        assert 'premier modèle' in page.locator('#fieldScope').inner_text()
        assert page.locator('.grid > .card').nth(1).locator('#ascan').count()==1
        pose=page.evaluate('window.BYTE_NDT.getPose()')
        assert abs(sum(v*v for v in pose['beam_direction_world'])-1)<1e-8
        m=pose['rotation_matrix_local_to_world']
        import numpy as np
        assert np.allclose(np.array(m).T@np.array(m),np.eye(3))
        assert abs(np.linalg.det(np.array(m))-1)<1e-8
        with page.expect_download() as vr: page.locator('#exportVR').click()
        assert vr.value.suggested_filename=='NOZZLE_VR_SCENE_V1.json'
        q=page.evaluate('surfaceProjection(point(az,z,R+2))')
        old_pose=page.evaluate('[az,z]')
        box=page.locator('#top').bounding_box()
        cx=box['x']+q[0]/720*box['width'];cy=box['y']+q[1]/430*box['height']
        page.mouse.move(cx,cy);page.mouse.down();page.mouse.move(cx+5,cy-12,steps=8);page.mouse.up();page.wait_for_timeout(80)
        assert page.evaluate('[az,z]')!=old_pose,'Surface probe did not move'
        assert abs(page.evaluate('Math.hypot(...point(az,z).slice(0,2))')-200)<1e-8
        page.locator('#reset').click()
        page.locator('#operatorSurface').select_option('unwrapped')
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
        previous=page.evaluate('lastPlanIndex');orientation=page.evaluate('heading')
        page.locator('#reverseScan').click()
        assert page.evaluate('playDirection')==-1
        assert page.evaluate('heading')==orientation,'Scan reversal rotated probe'
        page.locator('#demo').click();page.wait_for_timeout(90);page.locator('#pause').click()
        assert page.evaluate('lastPlanIndex')<previous,'Raster did not move backward'
        page.locator('#reverseScan').click()
        assert page.evaluate('playDirection')==1
        print('Raster reverse/resume independent of probe orientation: OK')
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
        page.locator('#operatorSurface').select_option('3d')
        surface_ms=page.evaluate('''()=>{const t=performance.now();for(let i=0;i<20;i++){heading=i;draw()}return (performance.now()-t)/20}''')
        print(f'Surface 3D redraw: {surface_ms:.1f} ms; radial position constraint: OK')
        page.screenshot(path='/workspace/nozzle_operator_check.png',full_page=True)
        browser.close()
    print('Nozzle browser: cylindrical rays, five-indication registry, drag, wheel, raster, pause, sample, export, exclusions, examination mode: OK')

if __name__=='__main__':main()
