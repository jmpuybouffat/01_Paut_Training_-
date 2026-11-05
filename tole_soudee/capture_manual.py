"""Capture the actual P03 views and export portable numerical exercise checks."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'manuals/assets'

def ready(page):
    page.wait_for_function("!motionBusy&&!motionPending&&!activeWorker&&lastComputedPose&&Math.abs(lastComputedPose.x-pose().x)<1e-5&&Math.abs(lastComputedPose.y-pose().y)<1e-5&&$('scatter').data?.length>1",timeout=60000)

def shot(page,id,name):
    page.locator('#'+id).first.scroll_into_view_if_needed()
    page.locator('#'+id).first.screenshot(path=str(OUT/(name+'.png')))

with sync_playwright() as p:
    b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
    page=b.new_page(viewport={'width':1500,'height':1100},device_scale_factor=1)
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content((ROOT/'operator.html').read_text(),timeout=60000);ready(page)
    checks={}
    for language in ['FR','EN']:
        page.locator('#'+language.lower()).click();ready(page)
        page.locator('#method').select_option('MWB');ready(page)
        page.locator('#preset').click();ready(page)
        page.locator('#resetFraming').click();ready(page)
        # Set the acquisition to a reproducible isolated witness pose.
        page.locator('#reset').click();page.locator('#calculate').click();ready(page)
        for id in ['scene','ascan','joint','section','field','scatter']:
            shot(page,id,language+'_'+id)
        page.locator('#plan').locator('..').screenshot(path=str(OUT/(language+'_plan.png')))
        checks[language+'_MWB']=page.evaluate("({pose:pose(),maxA:Math.max(...$('ascan').data[0].y),peakTime:$('ascan').data[0].x[$('ascan').data[0].y.indexOf(Math.max(...$('ascan').data[0].y))]})")
        page.locator('#xmin').fill('60');page.locator('#xmax').fill('70');page.locator('#ymin').fill('103');page.locator('#ymax').fill('105');page.locator('#ystep').fill('2');page.locator('#reset').click();page.locator('#raster').click()
        page.wait_for_function('!running&&records.length===12',timeout=60000)
        checks[language+'_raster_count']=page.evaluate('records.length')
        for id in ['bscan','map']:shot(page,id,language+'_'+id)
        page.locator('#method').select_option('PA');ready(page);shot(page,'sscan',language+'_sscan')
        checks[language+'_PA']=page.evaluate("({pose:pose(),angles:records.at(-1).angles,selected:profile().angle_deg})")
    assert not errors,errors
    (ROOT/'manuals/exercises_verified.json').write_text(json.dumps(checks,indent=2)+'\n')
    print('Captured actual P03 views FR/EN and checked 12-pose exercise raster.')
    b.close()
