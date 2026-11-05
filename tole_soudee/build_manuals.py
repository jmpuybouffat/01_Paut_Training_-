"""Generate self-contained bilingual P03 manuals and optionally their PDFs."""
from pathlib import Path
import argparse,base64,html,json,re
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'manuals'
CSS='''
*{box-sizing:border-box}body{font:16px/1.6 system-ui,Arial,sans-serif;color:#152c40;margin:0;background:#eaf0f5}main{max-width:1000px;margin:24px auto;background:white;padding:40px 55px}h1{font-size:40px;line-height:1.15;color:#103953}h2{font-size:25px;margin-top:36px;border-bottom:2px solid #27a6bc;padding-bottom:7px}h3{font-size:20px;margin-top:26px}p,li{max-width:90ch}a{color:#086d9b}code{font-size:.9em;background:#eef3f6;padding:2px 4px;overflow-wrap:anywhere}pre{background:#eef3f6;padding:16px;white-space:pre-wrap;font-size:13px}table{border-collapse:collapse;width:100%;margin:18px 0;font-size:14px}th,td{border:1px solid #c4d4df;padding:9px;vertical-align:top;text-align:left}th{background:#dcecf3}thead{display:table-header-group}figure{margin:24px 0;break-inside:avoid}figure img{display:block;width:100%;height:auto;border:1px solid #c4d4df}figcaption{font-size:13px;color:#385466;padding-top:7px}svg{max-width:100%;height:auto}nav{background:#f2f7fa;padding:16px 25px}nav li{margin:3px 0}.cover{padding:15px 0 20px}.lead{font-size:22px}.eyebrow{font-size:14px;color:#08788d;font-weight:700;letter-spacing:.06em}.muted{color:#567082;font-size:14px}.callout{background:#e5f6fa;border-left:5px solid #1694aa;padding:18px;margin:24px 0}.toolbar{position:sticky;top:0;z-index:1;background:#103953;color:white;padding:10px 20px;display:flex;gap:14px;align-items:center}.toolbar a{color:white}.toolbar button{padding:9px 14px;border:0;border-radius:4px;cursor:pointer}.smalltable{font-size:12px}.axes{background:#f5f9fb;border:1px solid #c4d4df;padding:12px}section{scroll-margin-top:65px}
@media(max-width:700px){main{margin:0;padding:20px}h1{font-size:30px}table{font-size:12px}}
@media print{@page{size:A4;margin:16mm 14mm 18mm}body{background:white;font-size:10.5pt;line-height:1.42}main{max-width:none;margin:0;padding:0}.toolbar{display:none}.cover{break-after:page;padding-top:12mm}h1{font-size:32pt}h2{font-size:18pt;margin-top:18pt;break-after:avoid}h3{font-size:13pt;break-after:avoid}p,li{widows:3;orphans:3}table{font-size:9pt}th,td{padding:5pt}tr{break-inside:avoid}figure{margin:12pt 0;break-inside:avoid}figure img{max-height:91mm;object-fit:contain}figcaption{font-size:8.5pt}.smalltable{font-size:8pt}.lead{font-size:17pt}.eyebrow{font-size:10pt}.muted{font-size:9pt}nav{break-after:page}a{text-decoration:none;color:#103953}.axes{break-inside:avoid}pre{font-size:8.5pt}}
'''
CAPTIONS={
'FR':{'joint':'Préparation symétrique en X : quatre chanfreins et deux bourrelets. Le Z est global, orienté vers le haut.','plan':'Plan de palpage : sabot vert, émergence rouge, bande orange interdite. Les boutons locaux commandent X/Y.','scene':'CAO et rayon central au MWB45°, X65 / Y105,125 mm. Le contour bleu est l’encombrement provisoire, marge incluse.','ascan':'Pose MWB45° témoin, gain30 dB : réponse principale voisine de15,3 µs. Amplitude relative non étalonnée.','section':'Préparation en X et rayon réfléchi superposés ; la forme en V du rayon ne définit pas la préparation.','field':'Champ incident et réflexion de fond, rayon blanc ; profondeur zéro sur la face palpée.','scatter':'Champ diffusé calculé sur le même plan et la même référence de couleurs ; retour vers la sonde inclus.','sscan':'Exemple PA : sectoriel35–70°, pose X65 / Y100 mm, profondeur depuis TOP.','bscan':'Créneau d’exercice : 12 positions, numérotées horizontalement ; temps en µs.','map':'Cumul des réponses du même exercice : rétroprojection en X/Y/Z global, pas géométrie vraie des défauts.'},
'EN':{'joint':'Symmetric double-V (X) preparation: four bevels and two caps. Global Z points upwards.','plan':'Scanning plan: green wedge, red emergence point, orange excluded band. Local buttons control X/Y.','scene':'CAD and central ray at MWB45°, X65 / Y105.125 mm. Blue outline is the provisional footprint plus clearance.','ascan':'MWB45° witness pose,30 dB gain: main response near15.3 µs. Relative, uncalibrated amplitude.','section':'X preparation and reflected ray overlaid; the V-shaped ray does not define the joint preparation.','field':'Incident and backwall field with white ray; depth zero at the scanned face.','scatter':'Calculated scattered field on the same plane and colour reference, including return towards the probe.','sscan':'PA example:35–70° sector, X65 / Y100 mm, depth measured from TOP.','bscan':'Exercise raster:12 positions numbered horizontally; time in µs.','map':'Accumulated responses from the same exercise: global X/Y/Z backprojection, not true flaw geometry.'}}

def axes(lang):
    texts=['X : longitudinal','Y : transversal','Z : hors du plan','Vue de dessus schématique','Axe de soudure Y125'] if lang=='FR' else ['X: along weld','Y: across weld','Z: out of plane','Schematic plan view','Weld axis Y125']
    return f'''<div class="axes"><svg viewBox="0 0 620 255" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{texts[3]}"><defs><marker id="arr" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0 0L6 3L0 6Z" fill="#17394f"/></marker></defs><rect x="65" y="35" width="380" height="150" fill="#d9e5ee" stroke="#42687f"/><path d="M65 110H445" stroke="#dc8a33" stroke-width="17"/><path d="M65 185H500M65 185V12" stroke="#17394f" stroke-width="2" marker-end="url(#arr)"/><path d="M65 185H500" stroke="#17394f" stroke-width="2" marker-end="url(#arr)"/><text x="200" y="213" font-size="16">{texts[0]}</text><text x="72" y="21" font-size="16">{texts[1]}</text><text x="120" y="103" font-size="15">{texts[4]}</text><circle cx="65" cy="185" r="7" fill="white" stroke="#17394f"/><circle cx="65" cy="185" r="2" fill="#17394f"/><text x="20" y="241" font-size="15">{texts[2]} · 245 × 250 × 10 mm</text><text x="460" y="170" font-size="14">Y0</text><text x="450" y="48" font-size="14">Y250</text></svg></div>'''

def palette(lang):
    colors=['#06145b','#003dcc','#00baff','#00d889','#ffff00','#ff7b00','#d80000']
    stops=''.join(f'<stop offset="{i/6:.4f}" stop-color="{c}"/>' for i,c in enumerate(colors))
    caption='Amplitude relative : faible → forte' if lang=='FR' else 'Relative amplitude: low → high'
    return f'<figure><svg viewBox="0 0 700 85" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{caption}"><defs><linearGradient id="amplitude">{stops}</linearGradient></defs><rect x="20" y="8" width="650" height="28" fill="url(#amplitude)"/>'+''.join(f'<text x="{20+650*i/3:.2f}" y="60" text-anchor="{("start" if i==0 else "end" if i==3 else "middle")}" font-size="16">{v} dB</text>' for i,v in enumerate([-60,-40,-20,0]))+f'</svg><figcaption>{caption}. 20 log10(A/Aref).</figcaption></figure>'

def defects(lang):
    rows=json.loads((ROOT/'cad_exports/geometrie_pour_rv.json').read_text())['indications']
    names={'LACK_OF_FUSION':('Manque de fusion','Lack of fusion'),'SPHERICAL_INCLUSION_REFERENCE':('Inclusion sphérique','Spherical inclusion'),'SAWTOOTH_CRACK_REFERENCE':('Fissure dentelée','Sawtooth crack')}
    headers=['ID','Type','L × l / Ø mm','X','Y','Z','Rx / Ry / Rz °'] if lang=='FR' else ['ID','Type','L × W / Ø mm','X','Y','Z','Rx / Ry / Rz °']
    out='<table class="smalltable"><thead><tr>'+''.join('<th>'+x+'</th>' for x in headers)+'</tr></thead><tbody>'
    for row in rows:
        size=f"Ø {row['diameter_mm']:g}" if row['diameter_mm'] else f"{row['length_mm']:g} × {row['width_mm']:g}"
        cells=[row['id'],names[row['type']][lang=='EN'],size,*[f"{row[k]:g}" for k in ['x_mm','y_mm','z_mm']], ' / '.join(f"{row[k]:g}" for k in ['rx_deg','ry_deg','rz_deg'])]
        out+='<tr>'+''.join('<td>'+html.escape(x)+'</td>' for x in cells)+'</tr>'
    return out+'</tbody></table>'

def deploy(lang):
    names=['Dépôt / Repository','Branche / Branch','Fichier principal / Main file']
    values=['jmpuybouffat/01_Paut_Training_-','codex/tole-x-cao','plate_app.py']
    return '<table><tbody>'+''.join(f'<tr><th>{n}</th><td><code>{v}</code></td></tr>' for n,v in zip(names,values))+'</tbody></table><p><a href="https://github.com/jmpuybouffat/01_Paut_Training_-/tree/codex/tole-x-cao">GitHub · codex/tole-x-cao</a></p>'

def build(lang):
    body=(OUT/f'manual_{lang}.template.html').read_text()
    body=''.join(re.sub(r'([a-zà-ÿ])(?=[0-9])', r'\1 ',part) if i%2==0 else part for i,part in enumerate(re.split(r'(<[^>]+>)',body)))
    headings=re.findall(r'<section id="([^"]+)"><h2>(.*?)</h2>',body)
    toc='<ol>'+''.join(f'<li><a href="#{id}">{title}</a></li>' for id,title in headings)+'</ol>'
    for key,value in {'TOC':toc,'AXES':axes(lang),'PALETTE':palette(lang),'DEFECTS':defects(lang),'DEPLOY':deploy(lang)}.items():body=body.replace('@@'+key+'@@',value)
    count=0
    def figure(m):
        nonlocal count
        count+=1;id=m.group(1);data=base64.b64encode((OUT/'assets'/f'{lang}_{id}.png').read_bytes()).decode()
        return f'<figure><img alt="{html.escape(CAPTIONS[lang][id])}" src="data:image/png;base64,{data}"><figcaption>Fig. {count} — {CAPTIONS[lang][id]}</figcaption></figure>'
    body=re.sub(r'@@FIG:(\w+)@@',figure,body)
    assert '@@' not in body
    title='Manuel d’emploi — Tôle soudée P03' if lang=='FR' else 'User manual — Welded plate P03'
    filename='MANUEL_FR_P03' if lang=='FR' else 'USER_MANUAL_EN_P03'
    counterpart='USER_MANUAL_EN_P03.html' if lang=='FR' else 'MANUEL_FR_P03.html'
    toolbar=f'<div class="toolbar"><strong>P03 · '+('Manuel FR' if lang=='FR' else 'EN manual')+f'</strong><button onclick="window.print()">'+('Imprimer / PDF' if lang=='FR' else 'Print / PDF')+f'</button><a href="{counterpart}">'+('🇬🇧 English' if lang=='FR' else '🇫🇷 Français')+'</a></div>'
    result=f'<!doctype html><html lang="{lang.lower()}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{CSS}</style></head><body>{toolbar}<main>{body}</main></body></html>'
    target=OUT/(filename+'.html');target.write_text(result)
    print(f'{target.name}: {count} actual figures, {len(headings)} chapters, self-contained')
    return target

def pdf(paths):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        for path in paths:
            page=b.new_page();page.set_content(path.read_text(),timeout=60000);page.emulate_media(media='print');page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
            page.pdf(path=str(path.with_suffix('.pdf')),format='A4',print_background=True,prefer_css_page_size=True,display_header_footer=True,header_template='<span></span>',footer_template='<div style="font:9px Arial;width:100%;padding:0 14mm;color:#567082;display:flex;justify-content:space-between"><span>BYTE NDT · P03 · 2026-11-05</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
            page.close();print(path.with_suffix('.pdf').name)
        b.close()
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--pdf',action='store_true');args=parser.parse_args()
    paths=[build(lang) for lang in ['FR','EN']]
    if args.pdf:pdf(paths)
