"""Self-contained HTML/PDF Nozzle manuals; uses captured actual Nozzle views."""
from pathlib import Path
import argparse,base64,html,re,shutil,json
from style import CSS
ROOT=Path(__file__).resolve().parent
CAPTIONS={
'FR':{'geometry':'Vue de référence : tube principal et piquage à63°, courbes d’intersection et profils approchés.','top':'Surface3D au départ du cas témoin MWB45°/4MHz : point de sonde contraint à la paroi principale.','unwrapped':'Même pose sur le déroulé de la paroi : aide de déplacement secondaire.','focused':'Zoom sur MF1 : surface rose finie et lobes du champ calculé. Le trait orange est une référence sonde/cible.','section':'Coupe du champ scalaire par MF1 : abscisse Z, profondeur radiale en ordonnée, azimut fixé au défaut.','ascan':'PorteA0–20µs, gain10dB : témoin scalaire autour de8,73µs. Observer la réponse courante.','field':'Champ rétrodiffusé scalaire, référence fixe0,05, seuil d’affichage−40dB ; aucune réflexion de ce champ sur les parois.','teaching':'Ancien champ avec réflexions : représentation pédagogique, amplitudes heuristiques.','direct':'Champ direct scalaire de Green : normalisation par grille, sans champ réfléchi calculé.'},
'EN':{'geometry':'Reference geometry: main pipe and63° nozzle, intersection curves and approximate profiles.','top':'Initial MWB45°/4MHz witness pose on3D main-pipe surface.','unwrapped':'Same pose on the unwrapped wall, a secondary movement aid.','focused':'MF1 focus: finite pink surface and calculated scattering lobes. Orange line is a probe/target reference.','section':'Scalar section through MF1: horizontal global Z, vertical radial depth; azimuth fixed at the flaw.','ascan':'GateA0–20µs, gain10dB: scalar witness near8.73µs. Inspect the current response.','field':'Computed backscatter, fixed0.05 reference and−40dB display cutoff; no wall-bounce scattering.','teaching':'Historical reflected teaching field with heuristic amplitudes.','direct':'Direct scalar Green field, grid-normalized, without a computed reflected field.'}}

CAPTIONS['FR'].update({'PA_paIncident':'PA : champ incident déphasé et rayon direct dans la paroi cylindrique.','PA_field':'PA : champ rétrodiffusé de la même surface ; phases conservées jusqu’à la réception.','PA_ascan':'PA : A-scan du rayon45°, gain10dB0dB et porte0–20µs.','PA_paSector':'PA : secteur35–70° rétroprojeté dans Z/profondeur ; ce n’est pas une tomographie.','PA_paBscan':'PA : B-scan des points enregistrés, premier rayon35°.'})
CAPTIONS['EN'].update({'PA_paIncident':'PA: phased incident field and direct ray in the cylindrical wall.','PA_field':'PA: scattering from the same surface, retaining phase through reception.','PA_ascan':'PA: selected45° A-scan,30dB gain and0–20µs gate.','PA_paSector':'PA:35–70° backprojected Z/depth sector, not tomography.','PA_paBscan':'PA: B-scan of recorded samples, first35° ray.'})

def clean(s):return re.sub(r'([a-zà-ÿ])(?=[0-9])',r'\1 ',s)
def build(lang):
    body=(ROOT/f'manual_{lang}.template.html').read_text()
    body=''.join(clean(p) if i%2==0 else p for i,p in enumerate(re.split(r'(<[^>]+>)',body)))
    headings=re.findall(r'<section id="([^"]+)"><h2>(.*?)</h2>',body)
    witness=json.loads((ROOT/'witness_verified.json').read_text());amp=f"{witness[lang+'_PA']['event']['amp']:.4g}";body=body.replace('@@PAAMP@@',amp.replace('.',',') if lang=='FR' else amp)
    body=body.replace('@@TOC@@','<ol>'+''.join(f'<li><a href="#{id}">{title}</a></li>' for id,title in headings)+'</ol>')
    count=0
    def image(m):
        nonlocal count
        count+=1;id=m.group(1);caption=clean(CAPTIONS[lang][id]);data=base64.b64encode((ROOT/'assets'/f'{lang}_{id}.png').read_bytes()).decode()
        return f'<figure><img alt="{html.escape(caption)}" src="data:image/png;base64,{data}"><figcaption>Fig. {count} — {caption}</figcaption></figure>'
    body=re.sub(r'@@FIG:(\w+)@@',image,body);assert '@@' not in body
    title='Nozzle — Manuel FR REV0.5' if lang=='FR' else 'Nozzle — User manual EN REV0.5'
    filename='MANUEL_NOZZLE_FR' if lang=='FR' else 'NOZZLE_USER_MANUAL_EN'
    other='NOZZLE_USER_MANUAL_EN.html' if lang=='FR' else 'MANUEL_NOZZLE_FR.html'
    toolbar='<div class="toolbar"><strong>NOZZLE REV0.5</strong><button onclick="window.print()">'+('Imprimer / PDF' if lang=='FR' else 'Print / PDF')+f'</button><a href="{other}">'+('🇬🇧 English' if lang=='FR' else '🇫🇷 Français')+'</a></div>'
    target=ROOT/(filename+'.html');target.write_text(f'<!doctype html><html lang="{lang.lower()}"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{CSS}</style><body>{toolbar}<main>{body}</main></body></html>')
    print(f'{target.name}: {count} actual figures, {len(headings)} chapters');return target

def pdf(paths):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True,executable_path=shutil.which('chromium'),args=['--no-sandbox'])
        for path in paths:
            page=b.new_page();page.set_content(path.read_text(),timeout=60000);page.emulate_media(media='print');page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
            page.pdf(path=str(path.with_suffix('.pdf')),format='A4',prefer_css_page_size=True,print_background=True,display_header_footer=True,header_template='<span></span>',footer_template='<div style="font:9px Arial;width:100%;padding:0 14mm;color:#567082;display:flex;justify-content:space-between"><span>BYTE NDT · NOZZLE REV0.5 · 2026-11-05</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>');page.close();print(path.with_suffix('.pdf').name)
        b.close()
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--pdf',action='store_true');args=parser.parse_args();paths=[build(lang) for lang in ['FR','EN']]
    if args.pdf:pdf(paths)
