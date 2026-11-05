from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent
viewer=root/'cad_exports/CAD_TOLE_X_FR_EN.html'
if not viewer.exists():viewer=root.parent/'CAD_TOLE_X_FR_EN.html'
html=viewer.read_text()
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
 page=b.new_page(viewport=dict(width=1500,height=1100));errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(html,timeout=60000)
 page.wait_for_function('document.getElementById("view").data?.length===9',timeout=60000)
 page.locator('#en').click()
 assert page.locator('#title').inner_text()=='BYTE NDT — Double-V welded plate CAD'
 assert 'Lack of fusion' in page.locator('#flawTable').inner_text()
 assert 'HAZ' in page.locator('#hazText').inner_text()
 page.locator('#caps').uncheck();page.wait_for_function('document.getElementById("view").data.length===7')
 page.locator('#defects').check();page.wait_for_function('document.getElementById("view").data.length===12')
 page.locator('#caps').check();page.wait_for_function('document.getElementById("view").data.length===14')
 page.locator('#fr').click();assert 'Collage' in page.locator('#flawTable').inner_text()
 page.locator('#focus').click();page.wait_for_timeout(600)
 page.screenshot(path='/tmp/plate-cad-checked.png',full_page=True)
 assert not errors,errors
 print('Offline CAD viewer: 3D meshes, French/English flags, translated dimensions/flaws, visibility and weld focus: OK')
 b.close()
