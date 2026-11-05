"""Package only authorized plate assets, with checksums and no external paths."""
from pathlib import Path
import json,hashlib,zipfile
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent

def digest(data):return hashlib.sha256(data).hexdigest()
def package():
    files={}
    def add(name,path):files[name]=Path(path).read_bytes()
    add('OUVRIR_APPLICATION.html',ROOT/'operator.html')
    for name in ['MANUEL_FR_P03.pdf','USER_MANUAL_EN_P03.pdf','MANUEL_FR_P03.html','USER_MANUAL_EN_P03.html']:
        add(name,ROOT/'manuals'/name)
    add('STREAMLIT_DEMARRAGE_FR_EN.html',ROOT/'handoff/STREAMLIT_DEMARRAGE_FR_EN.html')
    for src,name in [('DEMARRER_FR.md','LIRE_MOI_FR.md'),('START_EN.md','READ_ME_EN.md'),('DEPLOY_FR_EN.md','DEPLOY_FR_EN.md'),('VERIFICATION_FR_EN.md','VERIFICATION_FR_EN.md')]:add(name,ROOT/'handoff'/src)
    for name in ['FABIEN_CAMERA_FR_EN.md','pose_camera_exemple.json']:add('FABIEN_CAMERA/'+name,ROOT/'handoff'/name)
    for p in sorted((ROOT/'cad_exports').rglob('*')):
        if p.is_file():add('CAO/'+p.relative_to(ROOT/'cad_exports').as_posix(),p)
    add('SOURCE/plate_app.py',REPO/'plate_app.py');add('SOURCE/requirements.txt',REPO/'requirements.txt')
    for name in ['build_operator.py','build_manuals.py','capture_manual.py','test_manuals.py','operator_template.html','plate_physics.js','manual_controls.js','view_controls.js','field_view.js','parameters.json','cad_model.py','make_viewer.py','requirements-cad.txt','test_plate_physics.js','test_operator_browser.py','test_manual_browser.py','test_views_browser.py','test_cad_model.py','test_viewer_browser.py','test_plate_streamlit.py']:
        add('SOURCE/tole_soudee/'+name,ROOT/name)
    add('SOURCE/tole_soudee/operator.html',ROOT/'operator.html')
    for p in sorted((ROOT/'manuals').rglob('*')):
        if p.is_file():add('SOURCE/tole_soudee/manuals/'+p.relative_to(ROOT/'manuals').as_posix(),p)
    add('SOURCE/tole_soudee/cad_exports/geometrie_pour_rv.json',ROOT/'cad_exports/geometrie_pour_rv.json')
    files['THIRD_PARTY.txt']=b'Plotly.js is bundled in the HTML files. Copyright Plotly, Inc. Distributed under the MIT license; see the embedded Plotly.js license header. CadQuery/OCP are optional offline CAD generation dependencies, not required to run the HTML.\n'
    manifest=[{'file':name,'bytes':len(data),'sha256':digest(data)} for name,data in sorted(files.items())]
    files['MANIFESTE_P03.json']=json.dumps(manifest,indent=2,ensure_ascii=False).encode()
    target=REPO/'downloads/BYTE_NDT_TOLE_P03_AVEC_MANUELS_FR_EN.zip'
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in files.items():z.writestr('BYTE_NDT_TOLE_P03/'+name,data)
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        for row in manifest:assert digest(z.read('BYTE_NDT_TOLE_P03/'+row['file']))==row['sha256']
    print(f'{target.name}: {len(files)} files, {target.stat().st_size} bytes; all checksums PASS')
if __name__=='__main__':package()
