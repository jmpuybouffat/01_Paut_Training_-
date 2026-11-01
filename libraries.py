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

PROBES = [dict(name=row['name'],frequency_MHz=row['frequency_MHz'],elements=1,pitch_mm=1.,active_elements=1,wedge_angle_deg=0.,mode='T',refracted_angle_deg=row['refracted_angle_deg']) for row in MWB_PROBES]
