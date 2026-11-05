"""Verify the separate Streamlit entry including its real iframe worker."""
from pathlib import Path
import subprocess,time,urllib.request
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
proc=subprocess.Popen(['/workspace/nozzle-venv/bin/python','-m','streamlit','run','plate_app.py','--server.port','8514','--server.headless','true','--browser.gatherUsageStats','false'],cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
    for _ in range(100):
        try:
            if urllib.request.urlopen('http://127.0.0.1:8514/_stcore/health',timeout=1).status==200:break
        except OSError:time.sleep(.15)
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
        page=b.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto('http://127.0.0.1:8514',timeout=60000)
        frame=page.frame_locator('iframe').first
        frame.locator('#calculate').wait_for(timeout=60000)
        frame.locator('#calculate').click()
        frame.locator('#status').filter(has_text='amplitude').wait_for(timeout=60000)
        assert 'Contact valide' in frame.locator('#status').inner_text()
        frame.locator('#en').click()
        assert frame.locator('#calculate').inner_text()=='Calculate'
        assert not errors,errors
        b.close()
    print('Separate Streamlit entry: iframe, worker calculation, FR/EN: PASS')
finally:
    proc.terminate();proc.wait(timeout=10)
