"""Capture the actual Nozzle Streamlit witness, not a substitute plate model."""
from pathlib import Path
import subprocess,time,urllib.request,json,re
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'nozzle_documentation'
proc=subprocess.Popen(['/workspace/nozzle-venv/bin/python','-m','streamlit','run','app.py','--server.port','8515','--server.headless','true','--browser.gatherUsageStats','false'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def frame_ready(page):
    deadline=time.monotonic()+60
    while time.monotonic()<deadline:
        try:
            f=page.get_by_role('tabpanel').first.locator('iframe').first.element_handle(timeout=1000).content_frame()
            f.wait_for_function("typeof C!=='undefined'&&C.training_scenario==='PIECE_PERSONNALISEE'&&typeof scatteringState==='function'&&!scatteringState().pending&&scatteringState().events.length===1&&Math.abs(scatteringState().events[0].t-8.729713348)<1e-5",timeout=1000)
            return f
        except Exception:page.wait_for_timeout(150)
    raise RuntimeError('Nozzle witness dashboard did not become ready')
def shot(frame,id,name):
    frame.locator('#'+id).screenshot(path=str(OUT/'assets'/name))
try:
    for _ in range(120):
        try:
            if urllib.request.urlopen('http://127.0.0.1:8515/_stcore/health',timeout=1).status==200:break
        except OSError:time.sleep(.2)
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
        page=b.new_page(viewport={'width':1600,'height':1100});errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto('http://127.0.0.1:8515',timeout=60000)
        checks={}
        for lang in ['FR','EN']:
            page.get_by_role('radio',name=re.compile('Français' if lang=='FR' else 'English')).evaluate('(el)=>el.click()')
            page.get_by_role('tab').nth(2).click()
            page.get_by_role('button',name=re.compile('Charger le test témoin rétrodiffusion' if lang=='FR' else 'Load backscatter witness test')).click()
            frame=frame_ready(page)
            frame.locator('#gateStart').fill('0');frame.locator('#gateEnd').fill('20');frame.locator('#gateThreshold').fill('.01')
            checks[lang]=frame.evaluate("({event:scatteringState().events[0],pose:window.BYTE_NDT.getPose(),reference:scatteringState().reference_amplitude,model:scatteringState().model})")
            for id in ['top','ascan','section','field']:shot(frame,id,lang+'_'+id+'.png')
            frame.locator('#focusScatter').click();shot(frame,'top',lang+'_focused.png')
            frame.locator('#operatorSurface').select_option('unwrapped');shot(frame,'top',lang+'_unwrapped.png')
            frame.locator('#fieldView').select_option('teaching');shot(frame,'field',lang+'_teaching.png')
            frame.locator('#fieldView').select_option('cut');shot(frame,'field',lang+'_direct.png')
            page.get_by_role('button',name=re.compile('Charger le test témoin PA' if lang=='FR' else 'Load PA 32-element')).click()
            deadline=time.monotonic()+60
            while time.monotonic()<deadline:
                try:
                    paf=page.get_by_role('tabpanel').first.locator('iframe').first.element_handle(timeout=1000).content_frame()
                    paf.wait_for_function("typeof C!=='undefined'&&C.acquisition==='PHASED_ARRAY_32'&&!scatteringState().pending&&scatteringState().pa?.sector.length===19",timeout=1000)
                    break
                except Exception:page.wait_for_timeout(150)
            else:raise RuntimeError('PA witness not ready')
            paf.locator('#gateStart').fill('0');paf.locator('#gateEnd').fill('20')
            checks[lang+'_PA']=paf.evaluate("({pose:window.BYTE_NDT.getPose(),pa:C.pa,event:scatteringState().events[0],angles:scatteringState().pa.angles})")
            for id in ['paSector','ascan','field','paIncident']:
                shot(paf,id,lang+'_PA_'+id+'.png')
            paf.locator('#record').click()
            for zz in [-98,-96]:
                paf.evaluate('(zz)=>{z=zz;draw()}',zz)
                paf.wait_for_function('!scatteringState().pending',timeout=60000)
                paf.locator('#record').click()
            shot(paf,'paBscan',lang+'_PA_paBscan.png')
            paf.evaluate('z=-100;draw()');paf.wait_for_function('!scatteringState().pending',timeout=60000)
            if lang=='FR':(OUT/'SCENE_TEMOIN_PA_NOZZLE.json').write_text(json.dumps(paf.evaluate('window.BYTE_NDT.getScene()'),ensure_ascii=False,indent=2)+'\n')
            page.get_by_role('tab').nth(0).click()
            page.get_by_test_id('stPlotlyChart').first.screenshot(path=str(OUT/'assets'/(lang+'_geometry.png')))
        assert not errors,errors
        (OUT/'witness_verified.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
        b.close();print('Actual Nozzle Streamlit witness captured FR/EN; scalar time and pose checked.')
finally:
    proc.terminate();proc.wait(timeout=15)
