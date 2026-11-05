"""Check manual contents and offline illustrations; calculations are in other tests."""
from pathlib import Path
import json,re,subprocess
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent/'manuals'
expected=json.loads((ROOT/'exercises_verified.json').read_text())
assert expected['FR_raster_count']==expected['EN_raster_count']==12
assert expected['FR_MWB']['peakTime']==expected['EN_MWB']['peakTime']==15.3
assert expected['FR_MWB']['maxA']==expected['EN_MWB']['maxA']
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for name,lang in [('MANUEL_FR_P03','fr'),('USER_MANUAL_EN_P03','en')]:
        source=(ROOT/(name+'.html')).read_text();assert '@@' not in source
        page=b.new_page();page.set_content(source,timeout=60000)
        assert page.locator('html').get_attribute('lang')==lang
        assert page.locator('section[id]').count()==13
        assert page.locator('img').count()==10
        assert page.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
        assert page.evaluate("Array.from(document.querySelectorAll('nav a')).every(a=>document.querySelector(a.getAttribute('href')))")
        for word in ['plate_app.py','codex/tole-x-cao','MANTIS/GEKKO','35°','15.3' if lang=='en' else '15,3','applyTrackedPose','WELD_TOE']:
            assert word in page.locator('body').inner_text(),word
        text=subprocess.check_output(['pdftotext',str(ROOT/(name+'.pdf')),'-'],text=True)
        assert len(text)>15000
        assert 'plate_app.py' in text and 'MANTIS/GEKKO' in text
        assert '@@' not in text and not re.search(r'\bNaN\b',text)
        page.close()
    b.close()
print('Manuals: FR/EN, 13 chapters, 10 offline figures each, internal links, PDF text and checked exercise values: PASS')
