"""Parametric analytic double-V plate in mm. CAD only: no acoustic claims.

X is longitudinal, Y transverse and Z upward; the bottom plate face is Z=0.
Finish grooves are proposed visual geometry, separate from approved dimensions.
"""
from __future__ import annotations
import json, math, csv
from pathlib import Path
import cadquery as cq

ROOT=Path(__file__).resolve().parent


def load_parameters():
    return json.loads((ROOT/'parameters.json').read_text())


def derived(p):
    plate,joint,caps,haz=(p[k] for k in ('plate','joint','caps','haz'))
    L,W,T,axis=(plate[k] for k in ('length_x','width_y','thickness_z','weld_axis_y'))
    land,gap,angle=(joint[k] for k in ('land','gap','bevel_face_angle_deg'))
    if min(L,W,T,land,gap,caps['width'],caps['height'])<=0 or land>=T or not 0<angle<90:
        raise ValueError('Positive dimensions and a bevel between 0 and 90 degrees required')
    h=(T-land)/2;half=gap/2+h*math.tan(math.radians(angle))
    a=caps['width']/2;sag=caps['height'];radius=(a*a+sag*sag)/(2*sag)
    if half>=a:raise ValueError('Cap must cover the groove opening')
    lo,hi=axis-a,axis+a;hl,hr=lo-haz['width_from_cap_toe'],hi+haz['width_from_cap_toe']
    if not 0<hl<lo<axis<hi<hr<W:raise ValueError('HAZ and caps must fit within plate width')
    return dict(length=L,width=W,thickness=T,axis=axis,land_low=(T-land)/2,
                land_high=(T+land)/2,half_gap=gap/2,half_opening=half,
                opening=2*half,bevel_depth=h,cap_left=lo,cap_right=hi,
                haz_left=hl,haz_right=hr,cap_radius=radius)


def prism(points,length):
    return cq.Workplane('YZ').polyline(points).close().extrude(length).val()


def circular_caps(p,d):
    a,b,t,L=d['cap_left'],d['cap_right'],d['thickness'],d['length'];mid=d['axis'];h=p['caps']['height']
    top=(cq.Workplane('YZ').moveTo(a,t).threePointArc((mid,t+h),(b,t)).close().extrude(L).val())
    bottom=(cq.Workplane('YZ').moveTo(a,0).lineTo(b,0).threePointArc((mid,-h),(a,0)).close().extrude(L).val())
    return top,bottom


def finish_caps(top,bottom,p,d):
    r=p['ripples']
    if not r['enabled']:return top,bottom,0
    pitch,width,depth,bow=(r[k] for k in ('pitch','groove_width','depth','arc_bow'))
    if min(pitch,width,depth,bow)<=0 or width>=pitch or depth>=p['caps']['height']:
        raise ValueError('Invalid ripple finish dimensions')
    # A narrow, arc-shaped XY ribbon intersects only the outer cap skin.
    # Thus the groove follows the circular envelope at a shallow Z depth.
    ribbons=[];x=pitch/2
    while x+bow+width/2<d['length']:
        a,b,mid=d['cap_left'],d['cap_right'],d['axis']
        shape=(cq.Workplane('XY').workplane(offset=-p['caps']['height']-1)
          .moveTo(x-width/2,a).threePointArc((x+bow-width/2,mid),(x-width/2,b))
          .lineTo(x+width/2,b).threePointArc((x+bow+width/2,mid),(x+width/2,a))
          .close().extrude(d['thickness']+2*p['caps']['height']+2).val())
        ribbons.append(shape);x+=pitch
    cutters=cq.Compound.makeCompound(ribbons)
    top_skin=top.cut(top.translate((0,0,-depth)))
    bot_skin=bottom.cut(bottom.translate((0,0,depth)))
    return top.cut(top_skin.intersect(cutters)),bottom.cut(bot_skin.intersect(cutters)),len(ribbons)


COLORS={
 'TOLE_GAUCHE_EXT':(.60,.67,.72),'ZAT_GAUCHE':(.95,.68,.18),'TOLE_GAUCHE_RIVE':(.60,.67,.72),
 'METAL_FONDU_X':(.82,.40,.20),'TOLE_DROITE_RIVE':(.60,.67,.72),'ZAT_DROITE':(.95,.68,.18),
 'TOLE_DROITE_EXT':(.60,.67,.72),'BOURRELET_SUPERIEUR':(.82,.40,.20),'BOURRELET_INFERIEUR':(.82,.40,.20)}
STEP_NAMES_EN={'TOLE_GAUCHE_EXT':'BASE_LEFT_OUTER','ZAT_GAUCHE':'HAZ_LEFT','TOLE_GAUCHE_RIVE':'BASE_LEFT_WELD_SIDE','METAL_FONDU_X':'DOUBLE_V_WELD_METAL','TOLE_DROITE_RIVE':'BASE_RIGHT_WELD_SIDE','ZAT_DROITE':'HAZ_RIGHT','TOLE_DROITE_EXT':'BASE_RIGHT_OUTER','BOURRELET_SUPERIEUR':'TOP_REINFORCEMENT','BOURRELET_INFERIEUR':'BOTTOM_REINFORCEMENT'}
LABELS={
 'TOLE_GAUCHE_EXT':('Tôle gauche — partie extérieure','Left plate — outer region'),
 'ZAT_GAUCHE':('Zone affectée thermiquement gauche','Left heat-affected zone'),
 'TOLE_GAUCHE_RIVE':('Tôle gauche — rive','Left plate — weld-side region'),
 'METAL_FONDU_X':('Métal fondu — préparation en X','Weld metal — double-V preparation'),
 'TOLE_DROITE_RIVE':('Tôle droite — rive','Right plate — weld-side region'),
 'ZAT_DROITE':('Zone affectée thermiquement droite','Right heat-affected zone'),
 'TOLE_DROITE_EXT':('Tôle droite — partie extérieure','Right plate — outer region'),
 'BOURRELET_SUPERIEUR':('Bourrelet supérieur','Top reinforcement'),
 'BOURRELET_INFERIEUR':('Bourrelet inférieur','Bottom reinforcement')}


def build(p=None,finish=True):
    p=load_parameters() if p is None else p;d=derived(p)
    L,W,T,a,gl,gh,hg,ho=(d[k] for k in ('length','width','thickness','axis','land_low','land_high','half_gap','half_opening'))
    yl,yr,hl,hr=(d[k] for k in ('cap_left','cap_right','haz_left','haz_right'))
    def rect(y0,y1):return prism([(y0,0),(y1,0),(y1,T),(y0,T)],L)
    parts={
      'TOLE_GAUCHE_EXT':rect(0,hl),
      'ZAT_GAUCHE':rect(hl,yl),
      'TOLE_GAUCHE_RIVE':prism([(yl,0),(a-ho,0),(a-hg,gl),(a-hg,gh),(a-ho,T),(yl,T)],L),
      'METAL_FONDU_X':prism([(a-ho,0),(a+ho,0),(a+hg,gl),(a+hg,gh),(a+ho,T),(a-ho,T),(a-hg,gh),(a-hg,gl)],L),
      'TOLE_DROITE_RIVE':prism([(a+ho,0),(yr,0),(yr,T),(a+ho,T),(a+hg,gh),(a+hg,gl)],L),
      'ZAT_DROITE':rect(yr,hr),
      'TOLE_DROITE_EXT':rect(hr,W)}
    top,bottom=circular_caps(p,d)
    count=0
    if finish:top,bottom,count=finish_caps(top,bottom,p,d)
    parts['BOURRELET_SUPERIEUR']=top;parts['BOURRELET_INFERIEUR']=bottom
    for name,shape in parts.items():
        if not shape.isValid() or len(shape.Solids())!=1 or shape.Volume()<=0:
            raise ValueError('Invalid physical solid: '+name)
    return parts,dict(d,ripple_count_per_face=count)


def rotation_xyz(rx,ry,rz):
    """Rz(rz) Ry(ry) Rx(rx), degrees; local plane normal is initially +Z."""
    import numpy as np
    a,b,c=map(math.radians,(rx,ry,rz));ca,sa,cb,sb,cc,sc=math.cos(a),math.sin(a),math.cos(b),math.sin(b),math.cos(c),math.sin(c)
    return np.array([[cc*cb,cc*sb*sa-sc*ca,cc*sb*ca+sc*sa],
                     [sc*cb,sc*sb*sa+cc*ca,sc*sb*ca-cc*sa],[-sb,cb*sa,cb*ca]])


def example_indications(p,d):
    # Proposed locations are independent teaching examples, not measurements.
    inclination=90-p['joint']['bevel_face_angle_deg']
    z=7.5;y_right=d['axis']+d['half_gap']+(z-d['land_high'])*math.tan(math.radians(p['joint']['bevel_face_angle_deg']))
    y_left=2*d['axis']-y_right
    rows=[dict(id='MF1',type='LACK_OF_FUSION',length_mm=2.,width_mm=.5,diameter_mm=None,x_mm=65.,y_mm=y_left,z_mm=z,rx_deg=-inclination,ry_deg=0.,rz_deg=0.),
          dict(id='MF2',type='LACK_OF_FUSION',length_mm=4.,width_mm=.5,diameter_mm=None,x_mm=165.,y_mm=y_right,z_mm=z,rx_deg=inclination,ry_deg=0.,rz_deg=0.),
          dict(id='INC1',type='SPHERICAL_INCLUSION_REFERENCE',length_mm=None,width_mm=None,diameter_mm=.5,x_mm=105.,y_mm=d['cap_left']-5,z_mm=3.,rx_deg=0.,ry_deg=0.,rz_deg=0.),
          dict(id='INC2',type='SPHERICAL_INCLUSION_REFERENCE',length_mm=None,width_mm=None,diameter_mm=.5,x_mm=185.,y_mm=d['cap_right']+5,z_mm=7.,rx_deg=0.,ry_deg=0.,rz_deg=0.),
          dict(id='FIS1',type='SAWTOOTH_CRACK_REFERENCE',length_mm=2.,width_mm=.5,diameter_mm=None,x_mm=125.,y_mm=d['axis'],z_mm=3.,rx_deg=90.,ry_deg=0.,rz_deg=0.)]
    for row in rows:row.update(opening_mm=None,enabled=True,placement_status='PROPOSED_TEACHING_SCENARIO',rotation_convention='Rz_Ry_Rx_DEGREES',width_interpretation_status='TO_CONFIRM')
    return rows


def indication_shapes(rows):
    import numpy as np
    parts={}
    for r in rows:
        center=np.array([r[k] for k in ('x_mm','y_mm','z_mm')]);rot=rotation_xyz(*(r[k] for k in ('rx_deg','ry_deg','rz_deg')))
        if r['diameter_mm']:
            shape=cq.Solid.makeSphere(r['diameter_mm']/2,cq.Vector(*center),angleDegrees1=-90,angleDegrees2=90)
        else:
            l,w=r['length_mm'],r['width_mm']
            if r['type']=='SAWTOOTH_CRACK_REFERENCE':
                # One open-thickness reference FACE, not an air-gap solid.
                upper=[(-l/2+i*l/8,w/2-(.10 if i%2 else 0)) for i in range(9)]
                lower=[(x,y-(w-.10)) for x,y in reversed(upper)]
                xy=upper+lower
            else:xy=[(-l/2,-w/2),(l/2,-w/2),(l/2,w/2),(-l/2,w/2)]
            points=[cq.Vector(*(center+rot@np.array([x,y,0.]))) for x,y in xy]
            wire=cq.Wire.makePolygon(points,close=True);shape=cq.Face.makeFromWires(wire)
        if not shape.isValid():raise ValueError('Invalid reference geometry: '+r['id'])
        parts[r['id']]=shape
    return parts


def mesh_payload(parts):
    payload=[]
    for name,shape in parts.items():
        vertices,faces=shape.tessellate(.06,.18)
        payload.append(dict(id=name,label_fr=LABELS.get(name,(name,name))[0],label_en=LABELS.get(name,(name,name))[1],
                            vertices=[[v.x,v.y,v.z] for v in vertices],triangles=[list(f) for f in faces],color=COLORS.get(name,(.95,.15,.7))))
    return payload


def export_all(destination=None):
    out=ROOT/'cad_exports' if destination is None else Path(destination);out.mkdir(parents=True,exist_ok=True)
    p=load_parameters();parts,d=build(p,finish=True)
    assembly=cq.Assembly(name='BYTE_NDT_TOLE_X_REFERENCE')
    for name,shape in parts.items():assembly.add(shape,name=name,color=cq.Color(*COLORS[name]))
    assembly.export(str(out/'TOLE_X_245_250_10_ASSEMBLAGE.step'))
    english=cq.Assembly(name='BYTE_NDT_DOUBLE_V_PLATE_REFERENCE')
    for name,shape in parts.items():english.add(shape,name=STEP_NAMES_EN[name],color=cq.Color(*COLORS[name]))
    english.export(str(out/'WELDED_PLATE_X_245_250_10_ASSEMBLY_EN.step'))
    for name,shape in parts.items():cq.exporters.export(shape,str(out/(name+'.step')))
    smooth,_=build(p,finish=False);shape=cq.Compound.makeCompound(list(smooth.values()))
    cq.exporters.export(shape,str(out/'TOLE_X_ENVELOPPE_LISSE.step'))
    rows=example_indications(p,d);ref=indication_shapes(rows);refs=cq.Assembly(name='INDICATIONS_REFERENCES_NON_COUPANTES')
    for name,item in ref.items():refs.add(item,name=name,color=cq.Color(.95,.15,.7))
    refs.export(str(out/'INDICATIONS_REFERENCES_NON_COUPANTES.step'))
    (out/'parametres_et_geometrie.json').write_text(json.dumps(dict(parameters=p,derived=d),ensure_ascii=False,indent=2))
    with (out/'variations_indications.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    payload=mesh_payload(parts)
    (out/'geometrie_pour_rv.json').write_text(json.dumps(dict(schema='BYTE_NDT_PLATE_CAD_MESH_V1',units='mm',coordinate_system=p['coordinate_system'],millimetres_to_metres=.001,parts=payload,indication_reference_meshes=mesh_payload(ref),indications=rows),ensure_ascii=False,separators=(',',':')))
    return p,parts,d,payload,rows

if __name__=='__main__':
    p,parts,d,_,_=export_all();print(json.dumps(d,indent=2));print('Solids:',len(parts),'volume:',sum(s.Volume() for s in parts.values()))
