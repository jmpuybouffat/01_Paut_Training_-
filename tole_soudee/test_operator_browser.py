"""Operator flows, numeric integrity, FR/EN, stop and exam data separation."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent

def ready(page):
    page.wait_for_function("document.querySelector('#status').textContent.includes('amplitude') && document.getElementById('ascan').data?.length===1",timeout=60000)

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
    page=browser.new_page(viewport={'width':1500,'height':1100},accept_downloads=True)
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content((ROOT/'operator.html').read_text(),timeout=60000)
    ready(page)
    assert page.evaluate("$('ascan').data[0].y.some(x=>x>0)")
    assert page.evaluate("$('ascan').layout.xaxis.title.text")== 'µs'
    assert page.evaluate('records.length')==0
    page.locator('#calculate').click();ready(page)
    assert page.evaluate('records.length')==1
    values=page.evaluate("$('ascan').data[0].y")
    page.locator('#en').click();ready(page)
    assert page.evaluate("$('ascan').data[0].y")==values
    assert page.evaluate('records.length')==1
    assert 'Spherical inclusion' in page.locator('#defects').text_content()
    page.locator('#y').fill('125');page.locator('#calculate').click()
    page.wait_for_function("$('status').textContent.includes('WELD_TOE')")
    assert page.evaluate('records.length')==1
    assert page.evaluate("$('ascan').data.length")==0
    page.locator('#method').select_option('MWB');ready(page)
    assert page.evaluate('records.at(-1).profile.kind')=='MWB'
    page.locator('#method').select_option('PA');ready(page)
    assert page.evaluate('records.at(-1).angles[0]')==35
    assert page.evaluate('records.at(-1).angles.at(-1)')==70
    assert page.evaluate('records.at(-1).profile.pitch_mm')==.5
    assert page.evaluate('records.at(-1).profile.active_height_mm')==12
    assert page.evaluate("$('field').data.length")==2
    with page.expect_download() as d:page.locator('#export').click()
    export=Path('/tmp/plate-session-training.json');d.value.save_as(export)
    data=json.loads(export.read_text());assert data['truth'];assert data['acquisition'][-1]['pose6d']['position_mm']==[65,100,10]
    assert any(not a['contact'] for a in data['contact_events'])
    # finite raster, alternating direction, 2 mm steps along X
    page.locator('#reset').click()
    page.locator('#xmin').fill('64');page.locator('#xmax').fill('66');page.locator('#ymin').fill('99');page.locator('#ymax').fill('100');page.locator('#ystep').fill('1')
    page.locator('#raster').click()
    page.wait_for_function('!running && records.length===4',timeout=60000)
    assert page.evaluate('records.map(r=>r.pose.x)')==[64,66,66,64]
    page.locator('#raster').click();page.locator('#stop').click();n=page.evaluate('records.length');page.wait_for_timeout(800);assert page.evaluate('records.length')==n
    page.locator('#purpose').select_option('EXAM');ready(page)
    assert not page.locator('#truth').is_checked();assert not page.locator('#truthDetails').is_visible();assert not page.locator('#scenario').is_visible()
    page.locator('#calculate').click();ready(page)
    with page.expect_download() as d:page.locator('#export').click()
    export=Path('/tmp/plate-session-exam.json');d.value.save_as(export);data=json.loads(export.read_text());assert data['truth'] is None
    for r in data['acquisition']:
        for events in r['events']:
            for e in events:assert not {'id','model','position_from_truth_not_reconstruction','path'}.intersection(e)
    page.locator('#purpose').select_option('TRAINING');ready(page)
    page.locator('#method').select_option('SE');ready(page)
    page.locator('#cameraPanel summary').click()
    page.locator('#inputSource').select_option('CAMERA')
    accepted=page.evaluate("ByteNDTPlate.applyTrackedPose({sequence:1,timestamp_ms:10,confidence:.95,position_mm:[105,111,10],euler_xyz_deg:[0,0,90],face:'TOP'})")
    assert accepted['accepted'],accepted
    assert page.evaluate('records.at(-1).input_source')=='CAMERA'
    count=page.evaluate('records.length')
    rejected=page.evaluate("ByteNDTPlate.applyTrackedPose({sequence:2,timestamp_ms:11,confidence:.2,position_mm:[105,111,10],euler_xyz_deg:[0,0,90],face:'TOP'})")
    assert not rejected['accepted'];assert page.evaluate('records.length')==count
    rejected=page.evaluate("ByteNDTPlate.applyTrackedPose({sequence:3,timestamp_ms:12,confidence:.95,position_mm:[105,111,13],euler_xyz_deg:[0,0,90],face:'TOP'})")
    assert rejected['reason']=='LIFT_OR_TILT'
    page.locator('#inputSource').select_option('MANUAL')
    page.locator('#fr').click();ready(page)
    assert page.locator('#calculate').inner_text()=='Calculer'
    page.screenshot(path='/tmp/plate-operator-p01.png',full_page=True)
    assert not errors,errors
    browser.close()
    print('Operator browser: SE/MWB/PA, bilingual persistence, contact stops, fields/views, raster/stop, VR export, exam truth separation: PASS')
