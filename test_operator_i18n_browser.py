"""Check live operator labels, scan stop messages and field UI in English."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from test_operator_browser import configuration


def main():
 config=configuration();config['language']='EN'
 html=Path(__file__).with_name('nozzle_operator.html').read_text().replace('__CONFIG__',json.dumps(config))
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=browser.new_page(viewport=dict(width=1400,height=1200));errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html)
  assert page.locator('#reverseScan').inner_text()=='Reverse scan'
  assert page.locator('#demo').inner_text()=='Raster ▶'
  assert page.locator('#operatorSurface option:checked').inner_text().startswith('Nozzle 3D')
  text=page.locator('body').inner_text()
  for french in ['Inverser','Déplacer','Réinitialiser','Instructeur','Seuil','Champ avec réflexions']:
   assert french not in text,french
  page.locator('#fieldView').select_option('cut')
  assert 'scalar direct field' in page.locator('#fieldScope').inner_text()
  page.locator('#fieldView').select_option('teaching')
  page.locator('#instructor').check()
  assert 'Lack of fusion' in page.locator('#truth').inner_text()
  assert 'Collage' not in page.locator('#truth').inner_text()
  page.locator('#top').focus();page.keyboard.press('Escape')
  assert 'Stopped:' in page.locator('#scanLimit').inner_text()
  assert not errors,errors
  browser.close()
 print('English operator controls, options, field, indication labels and stop reason: OK')

if __name__=='__main__':main()
