"""Preserve actual zoom/camera across Y, X and full recalculation; verify field views."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent

def ready(page):
    page.wait_for_function("!motionBusy&&!motionPending&&!activeWorker&&lastComputedPose&&Math.abs(lastComputedPose.x-pose().x)<1e-5&&Math.abs(lastComputedPose.y-pose().y)<1e-5&&$('field').data?.length>1&&$('scatter').data?.length>1",timeout=60000)

with sync_playwright() as p:
    b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
    page=b.new_page(viewport={'width':1500,'height':1050});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content((ROOT/'operator.html').read_text(),timeout=60000);ready(page)
    page.locator('#method').select_option('MWB');ready(page)
    page.evaluate("""async()=>{await Plotly.relayout('scene',{'scene.camera':{eye:{x:1.8,y:-.8,z:1.2},center:{x:.1,y:0,z:0},up:{x:0,y:0,z:1}}});for(const id of ['field','scatter','section','sscan'])await Plotly.relayout(id,{'xaxis.range':[95,145],'yaxis.range':[9,1]});await Plotly.relayout('joint',{'xaxis.range':[115,135]});await Plotly.relayout('plan',{'xaxis.range':[30,100],'yaxis.range':[95,115]});await Plotly.relayout('ascan',{'xaxis.range':[0,20],'yaxis.range':[0,.2]});}""")
    snapshot=page.evaluate("Object.fromEntries(['scene','plan','field','scatter','joint','section','sscan','ascan'].map(id=>[id,id==='scene'?JSON.parse(JSON.stringify($(id)._fullLayout.scene.camera)):[$(id)._fullLayout.xaxis.range.slice(),$(id)._fullLayout.yaxis.range.slice()]]))")
    x0=page.evaluate('pose().x');y0=page.evaluate('pose().y')
    page.locator('#ystepminus').click();ready(page)
    assert abs(page.evaluate('pose().y')-(y0-1))<1e-6
    page.locator('#step').click();ready(page);assert abs(page.evaluate('pose().x')-(x0+1))<1e-6
    page.locator('#xstepminus').click();ready(page);assert abs(page.evaluate('pose().x')-x0)<1e-6
    # Also exercise the full CAD redraw, not just fast restyling.
    page.locator('#calculate').click();ready(page)
    after=page.evaluate("Object.fromEntries(['scene','plan','field','scatter','joint','section','sscan','ascan'].map(id=>[id,id==='scene'?JSON.parse(JSON.stringify($(id)._fullLayout.scene.camera)):[$(id)._fullLayout.xaxis.range.slice(),$(id)._fullLayout.yaxis.range.slice()]]))")
    def compare(a,b,path=''):
        if isinstance(a,dict):
            for k in a:compare(a[k],b[k],path+'.'+k)
        elif isinstance(a,list):
            for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+str(i))
        elif isinstance(a,(int,float)):assert abs(a-b)<1e-5,(path,a,b)
        else:assert a==b,(path,a,b)
    compare(snapshot,after)
    assert page.evaluate("$('field').data[0].colorscale") == page.evaluate("$('scatter').data[0].colorscale")
    assert page.evaluate("$('field').data[0].x")==list(range(70,181))
    for id in ['field','scatter']:
        assert page.evaluate(f"$('{id}').data[0].zmin")==-60
        assert page.evaluate(f"$('{id}').data[0].zmax")==0
        assert page.evaluate(f"$('{id}').data.some(t=>t.name==='Rayon central')")
    assert page.evaluate("$('scatter').data[0].z.flat().every(Number.isFinite)")
    assert page.evaluate("$('field').data[1].y[0]")==0
    assert page.evaluate("$('field').data[1].y[1]")==10
    page.locator('#resetFraming').click();ready(page)
    assert page.evaluate("$('field')._fullLayout.xaxis.range")==[70,180]
    page.locator('#en').click();ready(page)
    assert page.locator('#step').inner_text()=='X +1 mm'
    assert page.locator('#resetFraming').inner_text()=='Reset views'
    page.screenshot(path='/tmp/plate-p03-views.png',full_page=True)
    assert not errors,errors
    print('Stable framing on Y/X and full redraw, ±1 mm X, intentional reset, fixed palette/reference, ray on both physical fields and EN: PASS')
    b.close()
