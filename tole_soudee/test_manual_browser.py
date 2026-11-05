"""Exercise actual pointer capture and two-axis dragging, not simulated input values."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent

def settle(page):
    page.wait_for_function("!motionBusy && !motionPending && !activeWorker && document.getElementById('ascan').data?.length===1",timeout=60000)

def pixel(page,x,y):
    return page.evaluate("([x,y])=>{const p=$('plan'),l=p._fullLayout,r=p.getBoundingClientRect();return [r.left+l.xaxis._offset+l.xaxis.d2p(x),r.top+l.yaxis._offset+l.yaxis.d2p(y)]}",[x,y])

with sync_playwright() as p:
    b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
    page=b.new_page(viewport={'width':1500,'height':1050});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content((ROOT/'operator.html').read_text(),timeout=60000);settle(page)
    page.locator('#method').select_option('MWB');settle(page)
    page.locator('#plan').scroll_into_view_if_needed();start=pixel(page,65,105.125);end=pixel(page,75,101)
    page.mouse.move(*start);page.mouse.down();assert page.evaluate('dragActive')
    page.mouse.move(*end,steps=8)
    assert abs(page.evaluate('pose().x')-75)<.02
    assert abs(page.evaluate('pose().y')-101)<.02
    page.mouse.up();settle(page)
    assert abs(page.evaluate('lastComputedPose.x')-75)<.02
    assert abs(page.evaluate('records.at(-1).pose.y')-101)<.02
    assert page.evaluate("$('field').data.length")==2,'Full field refreshed after release'
    assert len(page.evaluate("$('joint').data[2].x"))==9
    assert page.evaluate("$('joint').data[2].y")==[0,0,4.375,5.625,10,10,5.625,4.375,0]
    assert page.evaluate("$('section').data.some(t=>t.name.includes('Préparation'))")
    page.locator('#moveYp').click();settle(page);assert abs(page.evaluate('pose().y')-102)<.02
    page.locator('#plan').focus();page.keyboard.press('ArrowDown');settle(page);assert abs(page.evaluate('pose().y')-101)<.02
    start=pixel(page,75,101);end=pixel(page,75,150)
    page.mouse.move(*start);page.mouse.down();page.mouse.move(*end,steps=10);page.mouse.up();settle(page)
    assert 110.99<=page.evaluate('pose().y')<=111.001,'Continuous motion must stop at left toe, not jump across weld'
    assert page.evaluate('PlatePhysics.bounds(config,pose(),profile()).ok')
    assert 'WELD_TOE' in page.locator('#status').inner_text()
    assert page.evaluate('records.every(r=>r.pose.y<=111.001)')
    page.locator('#en').click();settle(page)
    assert page.locator('#planWeld').inner_text()=='Weld zoom'
    page.locator('#planFull').click();assert page.evaluate("$('plan').layout.yaxis.range")==[0,250]
    page.locator('#planWeld').click();assert page.evaluate("$('plan').layout.yaxis.range")==[85,165]
    page.screenshot(path='/tmp/plate-p02-manual.png',full_page=True)
    assert not errors,errors
    print('Actual X/Y mouse drag, release-field refresh, Y buttons, keyboard, weld stop without crossing, rectangle, explicit X joint and EN zoom: PASS')
    b.close()
