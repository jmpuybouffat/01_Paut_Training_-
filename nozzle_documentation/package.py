"""Complete Nozzle REV0.5 delivery: runtime, manuals, scene and reproducibility."""
from pathlib import Path
import json,hashlib,zipfile
ROOT=Path(__file__).resolve().parents[1]
def sha(data):return hashlib.sha256(data).hexdigest()
def package():
 files={}
 def add(name,path):files[name]=Path(path).read_bytes()
 runtime=['app.py','geometry.py','libraries.py','scan.py','scan_access.py','acoustic_field.py','joint_profiles.py','i18n.py','nozzle_operator.html','operator_view.html','scalar_scattering.js','nozzle_array.js','nozzle_pa_extension.js','nozzle_training_standard.js','sync_nozzle_pa.py','requirements.txt','LANCER_NOZZLE.bat']
 for name in runtime:add(name,ROOT/name)
 for p in ROOT.glob('*.md'):add(p.name,p)
 for p in ROOT.glob('test_*.py'):add(p.name,p)
 add('test_nozzle_array.js',ROOT/'test_nozzle_array.js')
 for p in (ROOT/'nozzle_documentation').rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts:add('nozzle_documentation/'+p.relative_to(ROOT/'nozzle_documentation').as_posix(),p)
 for name in ['MANUEL_NOZZLE_FR.pdf','NOZZLE_USER_MANUAL_EN.pdf','MANUEL_NOZZLE_FR.html','NOZZLE_USER_MANUAL_EN.html']:add(name,ROOT/'nozzle_documentation'/name)
 add('LIRE_D_ABORD_FR_EN.html',ROOT/'nozzle_documentation/LIRE_D_ABORD_FR_EN.html')
 witness=json.loads((ROOT/'nozzle_documentation/witness_verified.json').read_text())
 reproducibility={'release':'NOZZLE_REV0_5_MWB_PA','training_standard':'BYTE_NDT_TRAINING_V1','scope':'REDUCED_SCALAR_NOT_ELASTICALLY_VALIDATED','source_sha256':{name:sha(files[name]) for name in runtime},'witness_cases':witness,'note':'Gain is dB; model echo times are us; reference amplitudes are not instrument calibrations. Camera integration remains with Fabien.'}
 files['REPRODUCTIBILITE_REPRODUCIBILITY.json']=json.dumps(reproducibility,indent=2,ensure_ascii=False).encode()
 manifest=[{'file':name,'bytes':len(data),'sha256':sha(data)} for name,data in sorted(files.items())]
 files['MANIFESTE_REV05.json']=json.dumps(manifest,indent=2).encode()
 target=ROOT/'downloads/BYTE_NDT_NOZZLE_REV0_5_MWB_PA_FR_EN.zip';target.parent.mkdir(exist_ok=True)
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,data in files.items():z.writestr('BYTE_NDT_NOZZLE_REV0_5/'+name,data)
 with zipfile.ZipFile(target) as z:
  assert z.testzip() is None
  for row in manifest:assert sha(z.read('BYTE_NDT_NOZZLE_REV0_5/'+row['file']))==row['sha256']
 print(f'{target.name}: {len(files)} files, {target.stat().st_size} bytes; all checksums PASS')
if __name__=='__main__':package()
