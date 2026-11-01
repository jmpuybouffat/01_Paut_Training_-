import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import json
from scan_access import scan_status
from scan import plan_scan, beam_segment
from geometry import validate_dimensions, preparation
from libraries import PROBES, INDICATIONS, MWB_PROBES, PROJECT_INDICATIONS

st.set_page_config(page_title='BYTE NDT | NOZZLE REV0.4', layout='wide')
lang=st.sidebar.radio('Langue / Language',['FR','EN'],horizontal=True)
def T(fr,en): return fr if lang=='FR' else en
workflow=st.sidebar.selectbox('Usage / Use',['TRAINING','REAL_EXAM_PREPARATION'])
st.sidebar.caption(T('Parcours : 1 Pièce 3D → 2 Réglages → 3 Scan manuel → 4 Notice.','Workflow: 1 3D specimen → 2 Setup → 3 Manual scan → 4 Guide.'))
st.sidebar.caption(T('Monoélément. Examen : préparation du dossier, procédure non validée.','Single element. Examination: dossier preparation, procedure not validated.'))
mouse_mode=st.sidebar.selectbox(T('Souris 3D','3D mouse'),['orbit','turntable','pan'])
if 'camera_revision' not in st.session_state: st.session_state.camera_revision=0
if st.sidebar.button(T('Réinitialiser la vue 3D','Reset 3D view')): st.session_state.camera_revision+=1
with st.sidebar.expander(T('Modules futurs — non actifs','Future modules — inactive')):
 scattering=st.sidebar.selectbox(T('Modèle de diffusion prévu','Planned scattering model'),['Kirchhoff','Born','GTD'])
 st.sidebar.caption(T('Modèles non implémentés : pas de calcul acoustique.','Models not implemented: no acoustic computation.'))
 procedure_revision=st.sidebar.text_input(T('Révision US 319 à vérifier','US 319 revision to verify'),'')
if workflow=='REAL_EXAM_PREPARATION': st.warning(T('Préparation seulement : procédure US 319 et cascade à documenter et valider.','Preparation only: US 319 procedure and cascade require documentation and validation.'))
st.title('BYTE NDT — NOZZLE GEOMETRY TWIN — REV0.4')
st.caption(T('Correctif ergonomie : piquage 3D en premier, réglages et scan séparés.','Usability correction: nozzle 3D first, setup and scan separated.'))
st.caption(T('Nozzle traversant • Pénétration complète • Préparation chanfreinée • Référence géométrique provisoire','Set-through nozzle • Full penetration • Bevel preparation • Provisional geometry reference'))
piece_tab,setup_tab,scan_tab,guide_tab=st.tabs([T('1 · Piquage 3D','1 · Nozzle 3D'),T('2 · Réglages de la pièce','2 · Specimen setup'),T('3 · Scan manuel','3 · Manual scan'),T('4 · Mode d’emploi','4 · User guide')])
with guide_tab.expander(T('Écran opérateur du premier twin — scan manuel, faisceau et rayons','Original twin operator screen — manual scan, beam and rays'),expanded=False):
 st.info(T('Fonctions reprises du twin FORMATION ALPHA : modèle historique de tôle soudée de 25 mm, 3 indications. Cette vue est indépendante des paramètres nozzle et des 5 indications de la pièce test. Référence historique, distincte du scan nozzle de l’onglet 3.','Restored FORMATION ALPHA functions: historical 25 mm welded-plate model, 3 indications. This view is independent of nozzle parameters and the 5 test-piece indications. Historical reference, separate from the nozzle scan in tab 3.'))
 components.html(Path(__file__).with_name('operator_view.html').read_text(encoding='utf-8'),height=2100,scrolling=True)
with st.sidebar:
 st.header(T('Tubes et intersection','Pipes and intersection'))
 D1=st.slider(T('Diamètre extérieur tube principal (mm)','Main pipe OD (mm)'),100.,1200.,400.,10.)
 t1=st.slider(T('Épaisseur tube principal (mm)','Main pipe thickness (mm)'),3.,60.,20.,1.)
 D2=st.slider(T('Diamètre extérieur nozzle (mm)','Nozzle OD (mm)'),30.,600.,160.,5.)
 t2=st.slider(T('Épaisseur nozzle (mm)','Nozzle thickness (mm)'),2.,50.,12.,1.)
 angle=st.slider(T('Angle entre axes (°)','Axis angle (°)'),25.,155.,63.,1.)
 offset=st.slider(T('Décalage transversal (mm)','Transverse offset (mm)'),-120.,120.,0.,5.)
 length=st.slider(T('Longueur tube principal (mm)','Main pipe length (mm)'),300.,1800.,800.,20.)
 nlen=st.slider(T('Longueur nozzle extérieure (mm)','External nozzle length (mm)'),100.,800.,320.,10.)
 st.header(T('Préparation du joint — hypothèses','Joint preparation — assumptions'))
 bevel=st.slider(T('Angle de chanfrein (°)','Bevel angle (°)'),0.,70.,35.,1.)
 gap=st.slider(T('Jeu nominal à la racine (mm)','Nominal root gap (mm)'),0.,8.,2.,.5)
 land=st.slider(T('Talon (mm)','Root land (mm)'),0.,12.,2.,.5)
 width=st.slider(T('Largeur nominale du cordon (mm)','Nominal weld width (mm)'),2.,50.,14.,1.)
 reinf=st.slider(T('Surépaisseur (mm)','Reinforcement (mm)'),0.,12.,3.,.5)
 st.header(T('Matériau (indicatif)','Material (indicative)'))
 mat=st.selectbox(T('Matériau','Material'),['Acier carbone','Inox austénitique','Aluminium','Personnalisé'],format_func=lambda x: {'Acier carbone':T('Acier carbone','Carbon steel'),'Inox austénitique':T('Inox austénitique','Austenitic steel'),'Aluminium':'Aluminium','Personnalisé':T('Personnalisé','Custom')}[x])
 presets={'Acier carbone':(5920,3240,7850),'Inox austénitique':(5790,3100,7900),'Aluminium':(6320,3130,2700),'Personnalisé':(5900,3200,7800)}
 vl0,vs0,rho0=presets[mat]
 vl=st.number_input('VL (m/s)',1000,9000,vl0,10)
 vs=st.number_input('VT (m/s)',500,6000,vs0,10)
 rho=st.number_input('ρ (kg/m³)',1000,15000,rho0,50)
 st.header(T('Affichage','Display'))
 inner=st.checkbox(T('Parois internes','Inner walls'),True)
 frames=st.checkbox(T('Normales et tangentes','Normals and tangents'),False)
 show_edges=st.checkbox(T('Courbes préparatoires illustratives','Illustrative preparation curves'),True)

errors=validate_dimensions(D1,t1,D2,t2,offset,land)
if errors:
 for fr,en in errors: st.error(T(fr,en))
 st.stop()
R=D1/2; r=D2/2; ri=r-t2; Ri=R-t1
alpha=np.deg2rad(angle)
u=np.array([np.sin(alpha),0.,np.cos(alpha)])
b=np.array([np.cos(alpha),0.,-np.sin(alpha)])
c=np.array([0.,1.,0.]); o=np.array([0.,offset,0.])

# For a surface of the nozzle at radius rad, solve intersection with main cylinder at radius target.
def intersection(rad,target,theta):
 q=o+rad*(np.cos(theta)[:,None]*b+np.sin(theta)[:,None]*c)
 A=u[0]**2+u[1]**2
 B=2*(q[:,0]*u[0]+q[:,1]*u[1]); C=q[:,0]**2+q[:,1]**2-target**2
 disc=B*B-4*A*C
 good=disc>=0
 s=np.full(len(theta),np.nan)
 s[good]=(-B[good]+np.sqrt(disc[good]))/(2*A)
 p=q+s[:,None]*u
 good &= np.isfinite(s) & (np.abs(p[:,2])<=length/2)
 p[~good]=np.nan
 return p,s,good

ths=np.linspace(0,2*np.pi,721)
outer,souter,okouter=intersection(r,R,ths)
root,sroot,okroot=intersection(r,Ri,ths)
# The nozzle starts at the root-intersection envelope. Only its external segment is shown.
# A masked surface prevents drawing the nozzle within the main pipe. This is a visual cut,
# not a CAD Boolean or verified weld solid.
fig=go.Figure()
def surface(x,y,z,name,color,opacity):
 fig.add_trace(go.Surface(x=x,y=y,z=z,name=name,showscale=False,opacity=opacity,colorscale=[[0,color],[1,color]],hoverinfo='skip'))

def main_wall(radius,name,color,opacity):
 zz=np.linspace(-length/2,length/2,80)[:,None]
 th=np.linspace(0,2*np.pi,160)[None,:]
 x=np.broadcast_to(radius*np.cos(th),(len(zz),th.shape[1])).copy()
 y=np.broadcast_to(radius*np.sin(th),(len(zz),th.shape[1])).copy()
 z=np.broadcast_to(zz,x.shape).copy()
 # The nozzle opening is a circular cut on the main pipe, centered on its own axis.
 p=np.stack([x,y,z],axis=-1)-o
 axial=np.sum(p*u,axis=-1)
 perpendicular=p-axial[...,None]*u
 # Only cut the branch-facing side of the main pipe. The infinite nozzle axis
 # also intersects the opposite side; cutting it creates a spurious second hole.
 outward_dot=(x*u[0]+y*u[1])/radius
 radial_depth=np.clip(np.sqrt(x*x+y*y)-Ri,0,t1)
 opening=r+gap+np.maximum(radial_depth-land,0)*np.tan(np.deg2rad(bevel))
 inside=(np.linalg.norm(perpendicular,axis=-1)<opening) & (outward_dot>0.05)
 x[inside]=np.nan;y[inside]=np.nan;z[inside]=np.nan
 surface(x,y,z,name,color,opacity)

main_wall(R,T('Tube principal extérieur','Main pipe outside'),'#90a9bd',.55)
if inner and Ri>0:main_wall(Ri,T('Tube principal intérieur','Main pipe inside'),'#587d93',.22)

ss=np.linspace(float(np.nanmin(sroot)),float(np.nanmax(souter))+nlen,180)[:,None]
tt=np.linspace(0,2*np.pi,180)[None,:]
def nozzle_wall(rad,name,color,opacity):
 s=np.broadcast_to(ss,(ss.shape[0],tt.shape[1]))
 theta=np.broadcast_to(tt,s.shape)
 p=o+s[...,None]*u+rad*(np.cos(theta)[...,None]*b+np.sin(theta)[...,None]*c)
 # Keep only nozzle wall outside the main pipe's OUTER cylindrical envelope.
 outside=(p[...,0]**2+p[...,1]**2 >= Ri**2-1e-6)
 # Limit to the outward half-space of the branch; negative-s backside is not a second nozzle.
 outside &= s>=0
 for k in range(3):p[...,k][~outside]=np.nan
 surface(p[...,0],p[...,1],p[...,2],name,color,opacity)
nozzle_wall(r,'Nozzle OD','#c6a27f',.74)
if inner and ri>0:nozzle_wall(ri,'Nozzle ID','#ad7e59',.23)

def curve(points,label,color,dash=None):
 fig.add_trace(go.Scatter3d(x=points[:,0],y=points[:,1],z=points[:,2],mode='lines',name=label,line=dict(color=color,width=7,dash=dash or 'solid')))
curve(outer,T('Intersection extérieure','Outer intersection'),'#d43c34')
curve(root,T('Intersection intérieure théorique (racine nominale)','Theoretical inner intersection (nominal root)'),'#00a39b')
# Preliminary edge curves are geometric offsets, NOT bevel-face or weld-toe solutions.
if show_edges:
 for sign,col,label in [(-1,'#e0a027',T('Bord côté principal — indicatif','Main-side edge — indicative')),(1,'#7e52b7',T('Bord côté nozzle — indicatif','Nozzle-side edge — indicative'))]:
  q=outer.copy(); good=np.isfinite(q).all(axis=1)
  normals=np.stack([q[:,0],q[:,1],np.zeros(len(q))],axis=-1)
  norms=np.linalg.norm(normals,axis=1)
  normals[good]/=norms[good,None]
  q[good]+=sign*(width/2)*normals[good]
  curve(q,label,col,'dash')
if frames:
 for i in range(0,len(outer),90):
  p=outer[i]
  if not np.isfinite(p).all():continue
  n1=np.array([p[0],p[1],0.]);n1/=np.linalg.norm(n1)
  q=p-o;n2=q-np.dot(q,u)*u;n2/=np.linalg.norm(n2)
  tan=np.cross(n1,n2)
  if np.linalg.norm(tan)<1e-8:continue
  tan/=np.linalg.norm(tan)
  for vec,color in [(n1,'#2666b6'),(n2,'#ba751a'),(tan,'#189b72')]:
   e=p+vec*35
   fig.add_trace(go.Scatter3d(x=[p[0],e[0]],y=[p[1],e[1]],z=[p[2],e[2]],mode='lines',line=dict(color=color,width=4),showlegend=False,hoverinfo='skip'))
# Physical dimensions affect these radial preparation surfaces; exact CAD remains out of scope.
face,cap=preparation(ths,Ri,R,r,offset,u,b,c,bevel,gap,land,reinf)
face[np.abs(face[...,2])>length/2]=np.nan
cap[np.abs(cap[...,2])>length/2]=np.nan
surface(face[...,0],face[...,1],face[...,2],T('Préparation radiale approchée','Approximate radial preparation'),'#e5b14c',.65)
surface(cap[...,0],cap[...,1],cap[...,2],T('Profil de renfort illustratif','Illustrative reinforcement profile'),'#dc8053',.8)

with piece_tab:
 st.subheader(T('Le piquage — vue de référence REV0.3 enrichie','Nozzle — enhanced REV0.3 reference view'))
 st.caption(T('Glisser pour tourner la pièce, molette pour zoomer. Cette vue conserve les tubes, les parois et les intersections. Le geste de la sonde est dans l’onglet 3.','Drag to rotate the specimen, wheel to zoom. This view retains pipes, walls and intersections. Probe manipulation is in tab 3.'))
 reference_fig=go.Figure(fig)
 reference_fig.update_layout(height=690,margin=dict(l=0,r=0,t=0,b=0),uirevision=f'reference-{st.session_state.camera_revision}',scene=dict(uirevision=f'reference-{st.session_state.camera_revision}',dragmode=mouse_mode,aspectmode='data',xaxis_title='X (mm)',yaxis_title='Y (mm)',zaxis_title='Z (mm)'),legend=dict(orientation='h'))
 st.plotly_chart(reference_fig,width='stretch',key='nozzle_reference',config={'scrollZoom':True,'displayModeBar':True,'displaylogo':False})
 st.info(T('Passer à 2 · Réglages pour préparer la pièce, puis à 3 · Scan manuel pour balayer.','Open 2 · Setup to prepare the specimen, then 3 · Manual scan to scan.'))
with setup_tab:
 st.subheader(T('Sondes MWB / compactes — accès au balayage','MWB / compact probes — scanning access'))
 st.info(T('Référence MWB et dimensions fabricant à renseigner. Ce contrôle compare les encombrements saisis ; il ne valide ni le contact courbe ni la couverture acoustique.','Enter MWB reference and manufacturer dimensions. This check compares entered clearances; it validates neither curved contact nor acoustic coverage.'))
 mwb_index=st.selectbox(T('Configuration MWB','MWB configuration'),range(len(MWB_PROBES)),format_func=lambda i:MWB_PROBES[i]['name'])
 mwb=MWB_PROBES[mwb_index]
 probe_data=dict(mwb,elements=1,active_elements=1)
 st.caption(T('Cette sélection MWB est utilisée par le scan manuel.','This MWB selection drives the manual scan.'))
 st.write(T('Angle réfracté nominal','Nominal refracted angle'),mwb['refracted_angle_deg'],'° ·',mwb['frequency_MHz'],'MHz')
 st.download_button(T('Exporter la bibliothèque MWB','Export MWB library'),json.dumps(MWB_PROBES,ensure_ascii=False,indent=2),'NOZZLE_REV0_4_MWB.json','application/json')
 probe_reference=st.text_input(T('Référence sonde / sabot','Probe / wedge reference'),mwb['name'],key=f'mwb_reference_{mwb_index}')
 st.caption(T('Déclarer chaque zone inaccessible et sa cause. Une zone non évaluée ne compte pas comme accessible ; un encombrement compatible ne prouve pas la couverture UT.','Declare each inaccessible zone and its reason. An unassessed zone does not count as accessible; a fitting footprint does not prove UT coverage.'))
 scan_rows=st.data_editor(pd.DataFrame([{'zone':'Zone 1','access':'UNASSESSED','reason':'','azimuth_start_deg':np.nan,'azimuth_end_deg':np.nan,'z_start_mm':np.nan,'z_end_mm':np.nan,'available_length_mm':0.,'available_width_mm':0.,'probe_length_mm':0.,'probe_width_mm':0.,'travel_mm':0.,'margin_mm':0.}]),num_rows='dynamic',hide_index=True,key='scan_access',column_config={'access':st.column_config.SelectboxColumn(T('Accès','Access'),options=['UNASSESSED','TO_ASSESS','INACCESSIBLE'],required=True)})
 scan_rows['assessment']=[scan_status(row) for row in scan_rows.to_dict('records')]
 for _,zone in scan_rows.iterrows():
  message=str(zone['zone'])+': '+zone['assessment']
  if zone['assessment']=='INACCESSIBLE':
   st.warning(message+' — '+str(zone['reason']))
   if not str(zone['reason']).strip(): st.caption(T('Préciser la cause de l’inaccessibilité.','Specify the reason for inaccessibility.'))
  else: st.write(message)
 st.caption(T('Les limites angulaires et axiales sont enregistrées pour repérer les zones ; aucune détection automatique de collision ni de couverture complète.','Angular and axial bounds are recorded to locate zones; no automatic collision detection or complete coverage assessment.'))
 st.download_button(T('Exporter les zones de balayage CSV','Export scan zones CSV'),scan_rows.assign(probe_reference=probe_reference).to_csv(index=False),'NOZZLE_REV0_4_SCAN_ZONES.csv','text/csv')

 st.subheader(T('Scan géométrique — tube principal','Geometric scan — main pipe'))
 st.caption(T('Trajet en méandre sur la surface extérieure. Les points sont planifiés, sans acquisition ni réponse UT. Zones non évaluées en orange, zones bloquées en rouge. Une zone inaccessible sans limites bloque tout le plan par précaution.','Serpentine path on the outer surface. Points are planned, without acquisition or UT response. Unassessed points are orange; blocked points red. An inaccessible zone without bounds blocks the entire plan conservatively.'))
 scan_a0=st.number_input(T('Azimut début (°)','Start azimuth (°)'),-360.,360.,-30.,1.)
 scan_a1=st.number_input(T('Azimut fin (°)','End azimuth (°)'),-360.,360.,30.,1.)
 scan_z0=st.number_input(T('Z début scan (mm)','Scan start Z (mm)'),-length/2,length/2,-min(100.,length/2),5.)
 scan_z1=st.number_input(T('Z fin scan (mm)','Scan end Z (mm)'),-length/2,length/2,min(100.,length/2),5.)
 scan_step=st.number_input(T('Pas de scan (mm)','Scan step (mm)'),1.,100.,10.,1.)
 scan_heading=st.number_input(T('Orientation du faisceau depuis +Z (°)','Beam heading from +Z (°)'),-180.,180.,0.,5.)
 scan_points=[]
 try:
  scan_points=plan_scan(R,length,scan_a0,scan_a1,scan_z0,scan_z1,scan_step,scan_rows.to_dict('records'))
 except ValueError as exc:
  st.error(T('Plan impossible : ','Cannot plan: ')+str(exc))
 if scan_points:
  # Exclude the prepared opening on the branch-facing main wall.
  for point in scan_points:
   xyz=np.array([point['X_mm'],point['Y_mm'],point['Z_mm']])
   delta=xyz-o
   perpendicular=delta-np.dot(delta,u)*u
   if np.dot(xyz[:2],u[:2])/R>0.05 and np.linalg.norm(perpendicular)<r+gap+max(t1-land,0)*np.tan(np.deg2rad(bevel)):
    point['status']='BLOCKED'
  scan_table=pd.DataFrame(scan_points)
  for status,color in [('PLANNED','#1baf89'),('UNASSESSED','#e4a626'),('BLOCKED','#e03b42')]:
   subset=scan_table[scan_table.status==status]
   if len(subset): fig.add_trace(go.Scatter3d(x=subset.X_mm,y=subset.Y_mm,z=subset.Z_mm,mode='markers',marker=dict(color=color,size=3),name='Scan '+status))
  st.write(T('Points du plan','Plan points'),len(scan_points),' · ',scan_table.status.value_counts().to_dict())
  scan_index=st.slider(T('Position de la sonde dans le plan','Probe position in plan'),0,max(1,len(scan_points)-1),0,1)
  current=scan_points[min(scan_index,len(scan_points)-1)]
  st.write(T('Position sélectionnée','Selected position'),current)
  if current['status']=='PLANNED':
   start=np.array([current['X_mm'],current['Y_mm'],current['Z_mm']])
   fig.add_trace(go.Scatter3d(x=[start[0]],y=[start[1]],z=[start[2]],mode='markers',marker=dict(size=9,color='#192bdb',symbol='diamond'),name=T('Sonde MWB — point d’entrée','MWB probe — entry point')))
   end=beam_segment(start,R,t1,mwb['refracted_angle_deg'],scan_heading)
   if end is not None and abs(end[2])<=length/2:
    curve(np.vstack([start,end]),T('Premier trajet géométrique','First geometric leg'),'#192bdb')
  else:
   st.warning(T('Position bloquée ou non évaluée : sonde et trajet non activés.','Blocked or unassessed position: probe and beam not activated.'))
  st.download_button(T('Exporter le plan de scan CSV','Export scan plan CSV'),scan_table.to_csv(index=False),'NOZZLE_REV0_4_SCAN_PLAN.csv','text/csv')
 st.caption(T('Le point d’entrée ne représente pas le volume du sabot. Pas de réflexion, collision CAO, amplitude, CAD/TCG ou classification cascade calculée.','Entry point does not represent wedge volume. No reflections, CAD collisions, amplitude, DAC/TCG or cascade classification calculated.'))

 st.subheader(T('Bibliothèque et placement des indications','Indication library and placement'))
 st.info(T('Paramètres de génération de pièces test : ajuster les dimensions et fixer les positions pour chaque variante. Les valeurs initiales sont des valeurs de départ.','Test-piece generation parameters: adjust dimensions and set positions for each variant. Initial values are starting values.'))
 specimen_name=st.text_input(T('Identifiant pièce test','Test piece identifier'),'PIECE_TEST_001')
 project_defaults=[dict(row,enabled=True,azimuth_deg=None,z_mm=None,depth_mm=None,orientation_deg=None) for row in PROJECT_INDICATIONS]
 project_table=st.data_editor(pd.DataFrame(project_defaults).astype({k:'float64' for k in ['length_mm','width_mm','diameter_mm','azimuth_deg','z_mm','depth_mm','orientation_deg']}),hide_index=True,num_rows='fixed',disabled=['id','type'],key='project_parameters')
 project_indications=json.loads(project_table.to_json(orient='records'))
 invalid_project=False
 for row in project_indications:
  if not row['enabled']: continue
  required=['diameter_mm'] if row['id']=='INC1' else ['length_mm','width_mm']
  if any(row[k] is None or not np.isfinite(float(row[k])) or float(row[k])<=0 for k in required):
   st.error(T('Dimensions positives requises pour ','Positive dimensions required for ')+row['id']); invalid_project=True
  for k in ['azimuth_deg','z_mm','depth_mm','orientation_deg']:
   if row[k] is not None and not np.isfinite(float(row[k])): invalid_project=True
  if row['depth_mm'] is not None and not 0<=float(row['depth_mm'])<=t1:
   st.error(T('Profondeur hors paroi : ','Depth outside wall: ')+row['id']); invalid_project=True
  if row['z_mm'] is not None and abs(float(row['z_mm']))>length/2:
   st.error(T('Position Z hors tube : ','Z position outside pipe: ')+row['id']); invalid_project=True
 pending=any(row[k] is None for row in project_indications if row['enabled'] for k in ['azimuth_deg','z_mm','depth_mm','orientation_deg'])
 st.caption(T('Les champs de position vides restent non définis dans l’export. Le placement sur les flancs nécessite encore une définition locale du joint.','Empty position fields remain undefined in the export. Placement on bevel faces still requires a local joint definition.'))
 specimen_config={'revision':'0.4','specimen_id':specimen_name,'status':'INVALID_PARAMETERS' if invalid_project else ('POSITIONS_PENDING' if pending else 'ILLUSTRATIVE_NOT_VALIDATED'),
  'scan_plan':{'surface':'MAIN_PIPE_OD','azimuth_start_deg':scan_a0,'azimuth_end_deg':scan_a1,'z_start_mm':scan_z0,'z_end_mm':scan_z1,'step_mm':scan_step,'beam_heading_deg':scan_heading,'points':scan_points},'plugins':{'cascade':{'status':'NOT_CONNECTED'},'CAD_TCG':{'status':'NOT_CONNECTED'}},
  'workflow':workflow,'acquisition':'MONO_ELEMENT','scattering':{'requested_model':scattering,'implemented':False},'procedure':{'reference':'US 319','revision':procedure_revision,'cascade_status':'DOCUMENT_REQUIRED_NOT_VALIDATED'},
  'geometry':{'main_OD_mm':D1,'main_thickness_mm':t1,'nozzle_OD_mm':D2,'nozzle_thickness_mm':t2,'axis_angle_deg':angle,'offset_mm':offset,'main_length_mm':length,'nozzle_length_mm':nlen},
  'joint':{'bevel_deg':bevel,'gap_mm':gap,'land_mm':land,'weld_width_mm':width,'reinforcement_mm':reinf},
  'material':{'name':mat,'VL_m_s':vl,'VT_m_s':vs,'density_kg_m3':rho},
  'mwb':dict(mwb,reference=probe_reference),'scan_zones':json.loads(scan_rows.to_json(orient='records')),'indications':project_indications}
 st.download_button(T('Exporter la configuration de la pièce test JSON','Export test-piece configuration JSON'),json.dumps(specimen_config,ensure_ascii=False,indent=2,allow_nan=False),'NOZZLE_REV0_4_TEST_PIECE.json','application/json',disabled=invalid_project)
with scan_tab:
 st.markdown('<a id="nozzle-manual-scan"></a>',unsafe_allow_html=True)
 st.subheader(T('Scan manuel du nozzle — écran opérateur','Nozzle manual scan — operator dashboard'))
 st.caption(T('Le plan technique de l’onglet 2 et le geste manuel sont deux écrans distincts. Dans ce panneau, la sonde se déplace à la souris.','The technical plan in tab 2 and manual operation are separate screens. Move the probe with the mouse in this panel.'))
 if pending: st.warning(T('Les positions des indications ne sont pas encore fixées : le faisceau est visible mais ces indications ne produisent pas de réponse A-scan. Compléter l’onglet 2.','Indication positions are not set yet: the beam is visible but these indications produce no A-scan response. Complete tab 2.'))
 operator_config=dict(specimen_config,language=lang)
 operator_json=json.dumps(operator_config,ensure_ascii=False,allow_nan=False).replace('<',chr(92)+'u003c')
 operator_html=Path(__file__).with_name('nozzle_operator.html').read_text(encoding='utf-8').replace('__CONFIG__',operator_json)
 components.html(operator_html,height=1550,scrolling=True)
with setup_tab.expander(T('Exemples exploratoires et diagnostic — avancé','Exploratory examples and diagnostics — advanced')):
 st.caption(T('Placement 3D exploratoire ci-dessous : exemples indépendants du registre projet.','Exploratory 3D placement below: examples independent of the project register.'))
 st.caption(T('Positions dans la paroi principale : azimut autour de Z, profondeur radiale depuis la surface extérieure. Aucune amplitude UT ni critère d’acceptation.','Positions in main wall: azimuth around Z, radial depth from outer surface. No UT amplitude or acceptance criterion.'))
 kind=st.selectbox(T('Type d’indication','Indication type'),range(len(INDICATIONS)),format_func=lambda i:INDICATIONS[i]['name'])
 example=dict(INDICATIONS[kind],azimuth_deg=0.,z_mm=0.,depth_mm=t1/2,orientation_deg=0.)
 indications=st.data_editor(pd.DataFrame([example]),num_rows='dynamic',key=f'indications_{kind}',hide_index=True)
 for idx,item in indications.iterrows():
  try:
   L,H,W=[float(item[k]) for k in ['length_mm','height_mm','width_mm']]
   depth=float(item['depth_mm']); zpos=float(item['z_mm']); az=np.deg2rad(float(item['azimuth_deg'])); orient=np.deg2rad(float(item['orientation_deg']))
   if not np.isfinite([L,H,W,depth,zpos,az,orient]).all() or min(L,H,W)<=0 or depth-H/2<0 or depth+H/2>t1 or abs(zpos)+max(L,W)/2>length/2 or item['shape'] not in ['Planar','Ellipsoid']: raise ValueError()
  except (ValueError,TypeError):
   st.error(T(f'Indication {idx+1} : dimensions ou position invalides',f'Indication {idx+1}: invalid dimensions or position')); continue
  normal=np.array([np.cos(az),np.sin(az),0.]); circum=np.array([-np.sin(az),np.cos(az),0.]); axial=np.array([0.,0.,1.])
  direction=np.cos(orient)*axial+np.sin(orient)*circum; transverse=np.cross(normal,direction)
  center=(R-depth)*normal+np.array([0.,0.,zpos])
  if item['shape']=='Planar':
   a,v=np.meshgrid(np.linspace(-1,1,2),np.linspace(-1,1,2))
   pts=center+a[...,None]*direction*L/2+v[...,None]*normal*H/2
  else:
   a,v=np.meshgrid(np.linspace(0,2*np.pi,35),np.linspace(0,np.pi,20))
   pts=center+np.sin(v)[...,None]*np.cos(a)[...,None]*direction*L/2+np.sin(v)[...,None]*np.sin(a)[...,None]*transverse*W/2+np.cos(v)[...,None]*normal*H/2
  surface(pts[...,0],pts[...,1],pts[...,2],str(item['name'])+f' #{idx+1}','#eb2275',1.)
 st.caption(T('Les indications sont des marqueurs locaux ; leur confinement exact et leur relation à la soudure ne sont pas validés.','Indications are local markers; exact containment and relation to the weld are not validated.'))
 st.download_button(T('Exporter sondes et indications JSON','Export probes and indications JSON'),json.dumps({'revision':'0.4','probe':probe_data,'indications':indications.to_dict('records'),'status':'ILLUSTRATIVE_NOT_VALIDATED'},ensure_ascii=False,indent=2),'NOZZLE_REV0_4_LIBRARIES.json','application/json')
 fig.update_layout(height=690,margin=dict(l=0,r=0,t=0,b=0),uirevision=f'camera-{st.session_state.camera_revision}',scene=dict(uirevision=f'camera-{st.session_state.camera_revision}',dragmode=mouse_mode,aspectmode='data',xaxis_title='X (mm)',yaxis_title='Y (mm)',zaxis_title='Z (mm)'),legend=dict(orientation='h'))
 left,right=st.columns([3,1])
 with left:st.plotly_chart(fig,width='stretch',key='nozzle_3d',config={'scrollZoom':True,'displayModeBar':True,'displaylogo':False})
 with right:
  st.subheader(T('État de validation','Validation status'))
  st.warning(T('REV0.4 : découpe VISUELLE uniquement. Les bords du chanfrein sont des décalages illustratifs ; ni volume soudé ni découpe CAO exacte ne sont validés.','REV0.4: VISUAL trimming only. Bevel edges are illustrative offsets; neither weld volume nor exact CAD Boolean is validated.'))
  st.metric(T('Points intersection extérieure','Outer intersection points'),int(okouter.sum()))
  st.metric(T('Points racine théorique','Theoretical root points'),int(okroot.sum()))
  st.write(T('**Joint retenu :** nozzle traversant, pleine pénétration, chanfrein de remplissage.','**Selected joint:** set-through nozzle, full penetration, fill bevel.'))
  st.write(T(f'Chanfrein {bevel}° · talon {land} mm · jeu {gap} mm · largeur {width} mm · surépaisseur {reinf} mm.',f'Bevel {bevel}° · land {land} mm · gap {gap} mm · width {width} mm · reinforcement {reinf} mm.'))
  st.caption(T('Le jeu, le talon, le chanfrein et le renfort pilotent une préparation radiale approchée, sans solide CAO validé.','Gap, land, bevel and reinforcement drive an approximate radial preparation, without a validated CAD solid.'))
  st.write(f'{mat} · VL {vl} m/s · VT {vs} m/s · ρ {rho} kg/m³')
  st.info(T('Valeurs matériaux indicatives. Vérification avec Jacques Marlier nécessaire.','Material values are indicative. Verification with Jacques Marlier is required.'))

with guide_tab:
 st.subheader(T('Parcours opérateur complet','Complete operator workflow'))
 if lang=='FR': st.markdown(Path(__file__).with_name('GUIDE_OPERATEUR_FR.md').read_text(encoding='utf-8'))
 st.download_button(T('Télécharger le mode d’emploi complet','Download complete French guide'),Path(__file__).with_name('GUIDE_OPERATEUR_FR.md').read_bytes(),'GUIDE_OPERATEUR_NOZZLE_FR.md','text/markdown')
 records=[]
 for label,pts in [('outer_intersection',outer),('nominal_root_inner_main_pipe',root)]:
  for i,p in enumerate(pts):
   if np.isfinite(p).all():records.append({'curve':label,'index':i,'theta_rad':ths[i],'X_mm':p[0],'Y_mm':p[1],'Z_mm':p[2]})
 export=pd.DataFrame(records)
 st.download_button(T('Exporter les courbes XYZ (CSV)','Export XYZ curves (CSV)'),export.to_csv(index=False).encode('utf-8'),'NOZZLE_REV0_4_REFERENCE_CURVES.csv','text/csv')
 parameters={'D_main_mm':D1,'t_main_mm':t1,'D_nozzle_mm':D2,'t_nozzle_mm':t2,'axis_angle_deg':angle,'offset_mm':offset,'length_main_mm':length,'length_nozzle_mm':nlen,'bevel_deg':bevel,'root_gap_mm':gap,'root_land_mm':land,'weld_width_mm':width,'reinforcement_mm':reinf,'material':mat,'VL_m_s':vl,'VT_m_s':vs,'density_kg_m3':rho,'status':'PROVISIONAL_NOT_VALIDATED'}
 st.download_button(T('Exporter fiche paramètres (CSV)','Export parameter sheet (CSV)'),pd.DataFrame([parameters]).to_csv(index=False).encode('utf-8'),'NOZZLE_REV0_4_JACQUES_MARLIER_PARAMETERS.csv','text/csv')
 with st.expander(T('📖 Notice d’emploi / limites','📖 User guide / limitations')):
  st.markdown(T('''**But.** Préparer la géométrie d’un nozzle traversant pour la revue avec Jacques Marlier.\n\n**Mode opératoire.** Régler les diamètres, épaisseurs, angle et décalage ; observer la découpe visuelle du nozzle ; afficher les courbes extérieure et de racine ; exporter les courbes et la fiche paramètres. Rotation à la souris, zoom à la molette.\n\n**Courbes.** Rouge : intersection des deux surfaces extérieures. Turquoise : intersection de la surface extérieure du nozzle avec la surface intérieure du tube principal (racine nominale purement géométrique). Les deux courbes de bord en pointillés sont des décalages illustratifs, PAS des limites de fusion calculées.\n\n**Limites.** Pas de découpe CAO booléenne ni de soudure volumique ; l’ouverture et les surfaces peuvent présenter des discontinuités d’affichage. Le chanfrein, le jeu, le talon et la surépaisseur modifient les surfaces approchées. Les indications sont des marqueurs géométriques ; aucun faisceau UT n’est calculé. Les cas obliques/excentrés exigent une vérification CAO.\n\n**Validation.** Aucune qualification industrielle. Faire confirmer le dessin du joint, la coupe intérieure, la racine et les dimensions réelles avant de figer la REV0.4.''','''**Purpose.** Prepare a set-through nozzle geometry for review with Jacques Marlier.\n\n**Instructions.** Adjust diameters, thicknesses, angle and offset; inspect the visually trimmed nozzle; display the outer and root curves; export curves and the parameter sheet. Rotate with mouse and zoom with wheel.\n\n**Curves.** Red: intersection of the two outer surfaces. Turquoise: nozzle outer surface intersecting main pipe inner surface (purely geometric nominal root). Dashed edge curves are illustrative offsets, NOT computed fusion boundaries.\n\n**Limitations.** No CAD Boolean or solid weld; openings and surfaces may have display discontinuities. Bevel, gap, land and reinforcement alter the approximate surfaces. Geometric indication markers only; no UT beams. Oblique/offset cases require CAD verification.\n\n**Validation.** Not industrially qualified. Confirm joint drawing, internal cut, root and actual dimensions before freezing REV0.4.'''))

 with st.expander(T('📚 Lexique technique FR / EN','📚 Technical glossary FR / EN')):
  glossary=[
  ('Nozzle traversant','Set-in / set-through nozzle','Piquage introduit dans une ouverture du tube principal.','Branch inserted into an opening in the main pipe.'),
  ('Nozzle posé','Set-on nozzle','Piquage assemblé sur le tube principal, sans traversée complète.','Branch attached to the main pipe without full insertion.'),
  ('Chanfrein','Bevel','Préparation inclinée du bord avant soudage.','Angled preparation of an edge before welding.'),
  ('Pleine pénétration','Complete joint penetration (CJP)','Pénétration du métal fondu sur toute l’épaisseur du joint.','Weld metal penetration through the full joint thickness.'),
  ('Talon','Root face / land','Partie non chanfreinée du bord préparé.','Unbeveled portion of the prepared edge.'),
  ('Jeu à la racine','Root opening / root gap','Écartement initial des éléments au niveau de la racine.','Initial separation of parts at the root.'),
  ('Racine','Weld root','Partie du joint située à l’opposé de la face de soudage.','Part of the joint opposite the welding face.'),
  ('Flanc de fusion','Fusion face','Surface du métal de base destinée à être fondue.','Base-metal surface intended to be fused.'),
  ('Surépaisseur','Weld reinforcement','Métal soudé dépassant le profil nominal de surface.','Weld metal above the nominal surface profile.'),
  ('Zone affectée thermiquement (ZAT)','Heat-affected zone (HAZ)','Métal de base non fondu dont les propriétés ont changé sous l’effet thermique.','Unmelted base metal whose properties changed due to welding heat.'),
  ('Bord du cordon','Weld toe','Jonction entre la face du cordon et le métal de base.','Junction between weld face and base metal.'),
  ('Indication volumique','Volumetric indication','Réponse associée à un réflecteur présentant un volume, comme une porosité.','Response associated with a three-dimensional reflector, such as porosity.'),
  ('Indication non volumique','Planar indication','Réponse associée à un réflecteur de type plan, comme une fissure.','Response associated with a planar reflector, such as a crack.')]
  st.dataframe(pd.DataFrame(glossary,columns=['FR','EN',T('Définition française','French definition'),T('Définition anglaise','English definition')]),hide_index=True,width='stretch')
  st.caption(T('La ZAT est définie dans le lexique, mais son étendue n’est pas calculée par ce modèle géométrique.','HAZ is defined in the glossary, but its extent is not calculated by this geometry model.'))
  st.download_button(T('Télécharger le lexique (CSV)','Download glossary (CSV)'),pd.DataFrame(glossary,columns=['FR','EN','Definition_FR','Definition_EN']).to_csv(index=False).encode('utf-8-sig'),'NOZZLE_REV0_4_GLOSSARY_FR_EN.csv','text/csv')

 with st.expander(T('Mode d’emploi REV0.4','REV0.4 user guide')):
  st.markdown(T('''1. Choisir TRAINING ou préparation d’examen réel et nommer la pièce test.
 2. Régler tubes, joint et matériau. Corriger les dimensions rejetées.
 3. Choisir la MWB monoélément : 45°, 60°, 70° ; 2, 4 ou 5 MHz. Saisir la référence réelle et les dimensions du sabot pour le contrôle d’accès.
 4. Déclarer les zones inaccessibles et leur cause. TO_ASSESS contrôle l’encombrement, sans démontrer la couverture UT.
 5. Régler les cinq indications et leurs positions. Les coordonnées vides restent non définies. Les exemples 3D sont indépendants du registre projet.
 6. Souris : glisser pour tourner (orbit), choisir pan pour déplacer, molette pour zoomer. Turntable limite les basculements. La caméra est conservée lors des changements de paramètres ; Réinitialiser la vue restaure la vue initiale. La barre Plotly fournit aussi les commandes de caméra.
 7. Exporter JSON et CSV. Ce sont des fiches de préparation, pas des résultats d’examen.
 8. Étapes suivantes : documenter la cascade suivant la révision applicable de US 319, étalonnage et critères ; intégrer et vérifier séparément Kirchhoff, Born et GTD. Ces moteurs ne sont pas implémentés.''','''1. Select TRAINING or real examination preparation and name the specimen.
 2. Set pipes, joint and material; resolve rejected dimensions.
 3. Select single-element MWB: 45°, 60°, 70°; 2, 4 or 5 MHz. Enter actual reference and wedge dimensions for access checks.
 4. Record inaccessible zones and reasons. TO_ASSESS checks footprint, not UT coverage.
 5. Set the five indications and positions. Empty coordinates remain undefined. 3D examples are independent of the project register.
 6. Mouse: drag to rotate (orbit), select pan to translate, wheel to zoom. Turntable limits tilting. Camera persists across parameter changes; Reset restores the initial view. Plotly toolbar provides camera controls too.
 7. Export JSON and CSV preparation sheets; these are not examination results.
 8. Next steps: document cascade using the applicable US 319 revision, calibration and criteria; integrate and verify Kirchhoff, Born and GTD separately. These engines are not implemented.'''))

 st.caption(T('Scan : saisir les limites des zones, choisir TO_ASSESS et renseigner les encombrements ; les points compatibles deviennent PLANNED. Choisir ensuite la position de sonde avec le curseur et exporter le plan. PLANNED ne signifie pas contrôlé.','Scan: enter zone bounds, select TO_ASSESS and fill footprint dimensions; compatible points become PLANNED. Select probe position with the slider and export the plan. PLANNED does not mean inspected.'))
