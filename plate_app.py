"""Separate plate entry point: the existing nozzle app.py remains unchanged."""
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(page_title='BYTE NDT · Welded plate',layout='wide')
p=Path(__file__).parent/'tole_soudee/operator.html'
if not p.exists():
    from tole_soudee.build_operator import build
    import plotly
    p=build(Path(plotly.__file__).parent/'package_data/plotly.min.js')
components.html(p.read_text(),height=1800,scrolling=True)
