"""Generic editable examples, not manufacturer specifications or acceptance rules."""
PROBES = [
 {'name':'PAUT linéaire 5 MHz / Linear PAUT','frequency_MHz':5.,'elements':64,'pitch_mm':0.6,'active_elements':16,'wedge_angle_deg':36.,'mode':'T','refracted_angle_deg':55.},
 {'name':'PAUT linéaire 2.25 MHz / Linear PAUT','frequency_MHz':2.25,'elements':32,'pitch_mm':1.,'active_elements':16,'wedge_angle_deg':36.,'mode':'T','refracted_angle_deg':45.},
 {'name':'UT droit 5 MHz / Straight UT','frequency_MHz':5.,'elements':1,'pitch_mm':10.,'active_elements':1,'wedge_angle_deg':0.,'mode':'L','refracted_angle_deg':0.}
]
INDICATIONS = [
 {'name':'Fissure / Crack','shape':'Planar','length_mm':10.,'height_mm':3.,'width_mm':0.3},
 {'name':'Manque de fusion / Lack of fusion','shape':'Planar','length_mm':15.,'height_mm':4.,'width_mm':0.5},
 {'name':'Porosité / Porosity','shape':'Ellipsoid','length_mm':3.,'height_mm':3.,'width_mm':3.},
 {'name':'Inclusion / Inclusion','shape':'Ellipsoid','length_mm':8.,'height_mm':2.,'width_mm':2.}
]

# User-specified MWB configurations. Angle is the nominal refracted angle,
# not the physical wedge angle. Dimensions require manufacturer data.
MWB_PROBES = [
 {'name':f'MWB {angle}° — {frequency} MHz', 'frequency_MHz':float(frequency),
  'mode':'T', 'refracted_angle_deg':float(angle), 'wedge_length_mm':None,
  'wedge_width_mm':None, 'status':'FOOTPRINT_PENDING'}
 for angle in (45,60,70) for frequency in (2,4,5)
]
PROJECT_INDICATIONS = [
 {'id':'MF1','type':'Collage / manque de fusion','length_mm':6.,'width_mm':3.,'diameter_mm':None,'location':'Flanc de préparation — position exacte à préciser'},
 {'id':'MF2','type':'Collage / manque de fusion','length_mm':6.,'width_mm':3.,'diameter_mm':None,'location':'Flanc de préparation — position exacte à préciser'},
 {'id':'INC1','type':'Inclusion','length_mm':None,'width_mm':None,'diameter_mm':2.,'location':'À préciser'},
 {'id':'FCT1','type':'Fissure de choc thermique','length_mm':4.,'width_mm':2.,'diameter_mm':None,'location':'À préciser'},
 {'id':'FCT2','type':'Fissure de choc thermique','length_mm':4.,'width_mm':2.,'diameter_mm':None,'location':'À préciser'}
]

for row in PROJECT_INDICATIONS:
 row['normal_tilt_deg']=45. if row['id']!='INC1' else 0.

PROBES = [dict(name=row['name'],frequency_MHz=row['frequency_MHz'],elements=1,pitch_mm=1.,active_elements=1,wedge_angle_deg=0.,mode='T',refracted_angle_deg=row['refracted_angle_deg']) for row in MWB_PROBES]

# Source nominale du premier twin ; pastille commune selon l’utilisateur.
# Aucune fiche catalogue constructeur n’a été vérifiée pour chaque fréquence.
for probe in MWB_PROBES:
 probe.update(manufacturer='Krautkrämer',family='MWB',active_width_mm=8.,active_height_mm=9.,active_size_source='Nominal inherited from first twin; common aperture per user; catalogue verification pending',catalogue_verified=False)

def gesture_demo_indications(thickness):
 """Synthetic main-wall targets for motion training, not weld-face locations."""
 placements=[(-24.,-70.,.25),(-12.,-55.,.4),(0.,-40.,.5),(12.,-25.,.6),(24.,-10.,.75)]
 return [dict(row,enabled=True,azimuth_deg=a,z_mm=z,depth_mm=thickness*depth,orientation_deg=0.,location='Cible artificielle en paroi principale — démo de geste, pas un flanc de soudure') for row,(a,z,depth) in zip(PROJECT_INDICATIONS,placements)]

# Données transcrites de la page catalogue fournie par l’utilisateur.
# La table visible couvre les versions 2 MHz ; ne pas extrapoler N aux 4/5 MHz.
for probe in MWB_PROBES:
 probe.update(body_length_mm=24.,body_width_mm=14.,body_height_mm=22.,body_dimensions_source='User-provided catalogue screenshot, Type 23 sketch; mounting orientation still to confirm')
 if probe['frequency_MHz']==2:
  a=int(probe['refracted_angle_deg'])
  probe.update(name=f'Krautkrämer MWB {a}-2ISO — 2 MHz',catalogue_model=f'MWB {a}-2ISO',catalogue_order_code={45:'0500041',60:'0500042',70:'0500043'}[a],near_field_mm=15.,active_size_source='User-provided catalogue screenshot: 2 MHz MWB table',catalogue_verified=True)
 else:
  probe.update(near_field_mm=None,catalogue_verified=False,catalogue_note='MWB45-4 waveform shown, but full 4/5 MHz specification table not provided')
