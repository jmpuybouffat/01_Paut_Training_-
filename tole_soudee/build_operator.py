"""Build the self-contained training prototype. No CAD dependency at runtime."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def build(plotly_js):
    template=(ROOT/'operator_template.html').read_text()
    values={'VIEW_CONTROL':(ROOT/'view_controls.js').read_text(),'FIELD_VIEW':(ROOT/'field_view.js').read_text(),'MANUAL_CONTROL':(ROOT/'manual_controls.js').read_text(),'PLOTLY':Path(plotly_js).read_text(),'PHYSICS':(ROOT/'plate_physics.js').read_text(),'PARAMETERS':json.dumps(json.loads((ROOT/'parameters.json').read_text())),'MESH':(ROOT/'cad_exports/geometrie_pour_rv.json').read_text()}
    for key,value in values.items(): template=template.replace('@@'+key+'@@',value)
    target=ROOT/'operator.html';target.write_text(template);return target
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--plotly-js',required=True);a=p.parse_args();print(build(a.plotly_js))
