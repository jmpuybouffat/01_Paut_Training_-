"""Separate welded-plate service; the existing nozzle app.py stays independent."""
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

ROOT=Path(__file__).resolve().parent
DOCS=ROOT/'tole_soudee/manuals'
st.set_page_config(page_title='BYTE NDT · Welded plate P03',layout='wide')
st.caption('P03 · 🇫🇷 Formation soudure / 🇬🇧 Weld inspection training')
for col,(name,label) in zip(st.columns(2),[
    ('MANUEL_FR_P03.pdf','📘 Manuel français · PDF'),
    ('USER_MANUAL_EN_P03.pdf','📗 English user manual · PDF'),
]):
    path=DOCS/name
    if path.exists():
        col.download_button(label,path.read_bytes(),file_name=name,mime='application/pdf',key=name,on_click='ignore',use_container_width=True)
with st.expander('Manuels HTML / HTML manuals · Fabien'):
    for name,label in [('MANUEL_FR_P03.html','🇫🇷 Manuel illustré HTML'),('USER_MANUAL_EN_P03.html','🇬🇧 Illustrated HTML manual')]:
        path=DOCS/name
        if path.exists():st.download_button(label,path.read_bytes(),file_name=name,mime='text/html',key=name,on_click='ignore')
    st.markdown('[Dossier caméra Fabien / Camera integration guide](https://github.com/jmpuybouffat/01_Paut_Training_-/blob/codex/tole-x-cao/tole_soudee/handoff/FABIEN_CAMERA_FR_EN.md)')
p=ROOT/'tole_soudee/operator.html'
if not p.exists():
    from tole_soudee.build_operator import build
    import plotly
    p=build(Path(plotly.__file__).parent/'package_data/plotly.min.js')
components.html(p.read_text(),height=1800,scrolling=True)
