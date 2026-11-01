"""UI translations, retaining canonical keys/values for computation and exports."""
VALUES = {
 'type':{
  'Collage / manque de fusion':('Collage / manque de fusion','Lack of fusion'),
  'Inclusion':('Inclusion','Inclusion'),
  'Fissure de choc thermique':('Fissure de choc thermique','Thermal shock crack')},
 'location':{
  'Flanc de préparation — position exacte à préciser':('Flanc de préparation — position exacte à préciser','Preparation face — exact position pending'),
  'À préciser':('À préciser','To be specified'),
  'Cible artificielle en paroi principale — démo de geste, pas un flanc de soudure':('Cible artificielle en paroi principale — démo de geste, pas un flanc de soudure','Artificial main-wall target — motion demo, not a weld face')},
 'name':{
  'Fissure / Crack':('Fissure','Crack'),
  'Manque de fusion / Lack of fusion':('Manque de fusion','Lack of fusion'),
  'Porosité / Porosity':('Porosité','Porosity'),
  'Inclusion / Inclusion':('Inclusion','Inclusion')},
 'shape':{'Planar':('Plane','Planar'),'Ellipsoid':('Ellipsoïde','Ellipsoid')},
 'access':{'UNASSESSED':('Non évalué','Unassessed'),'TO_ASSESS':('Évaluer l’encombrement','Assess footprint'),'INACCESSIBLE':('Inaccessible','Inaccessible')}
}
COLUMNS={
 'id':('ID','ID'),'type':('Type','Type'),'name':('Nom','Name'),'shape':('Forme','Shape'),
 'length_mm':('Longueur (mm)','Length (mm)'),'width_mm':('Largeur (mm)','Width (mm)'),
 'height_mm':('Hauteur (mm)','Height (mm)'),'diameter_mm':('Diamètre (mm)','Diameter (mm)'),
 'location':('Emplacement','Location'),'enabled':('Activée','Enabled'),
 'azimuth_deg':('Azimut (°)','Azimuth (°)'),'z_mm':('Position Z (mm)','Z position (mm)'),
 'depth_mm':('Profondeur (mm)','Depth (mm)'),'orientation_deg':('Orientation (°)','Orientation (°)'),
 'zone':('Zone','Zone'),'access':('Accès','Access'),'reason':('Motif','Reason'),
 'azimuth_start_deg':('Azimut début (°)','Start azimuth (°)'),
 'azimuth_end_deg':('Azimut fin (°)','End azimuth (°)'),
 'z_start_mm':('Z début (mm)','Start Z (mm)'),'z_end_mm':('Z fin (mm)','End Z (mm)'),
 'available_length_mm':('Longueur disponible (mm)','Available length (mm)'),
 'available_width_mm':('Largeur disponible (mm)','Available width (mm)'),
 'probe_length_mm':('Longueur sabot (mm)','Wedge length (mm)'),
 'probe_width_mm':('Largeur sabot (mm)','Wedge width (mm)'),
 'travel_mm':('Course (mm)','Travel (mm)'),'margin_mm':('Marge (mm)','Margin (mm)')}
STATUS={'UNASSESSED':('Non évalué','Unassessed'),'TO_ASSESS':('À évaluer','To assess'),
 'INACCESSIBLE':('Inaccessible','Inaccessible'),'INSUFFICIENT_CLEARANCE':('Encombrement insuffisant','Insufficient clearance'),
 'FOOTPRINT_FITS_ONLY':('Encombrement compatible uniquement','Footprint fits only'),
 'PLANNED':('Planifié','Planned'),'BLOCKED':('Bloqué','Blocked'),'OPENING':('Ouverture du piquage','Nozzle opening')}


def canonical_value(column,value):
 if not isinstance(value,str):return value
 for key,translations in VALUES.get(column,{}).items():
  if value==key or value in translations:return key
 return value


def display_value(column,value,lang):
 key=canonical_value(column,value)
 pair=VALUES.get(column,{}).get(key) if isinstance(key,str) else None
 return pair[0 if lang=='FR' else 1] if pair else value


def translate_rows(rows,lang,canonical=False):
 return [{k:(canonical_value(k,v) if canonical else display_value(k,v,lang)) for k,v in row.items()} for row in rows]


def column_label(column,lang):return COLUMNS.get(column,(column,column))[0 if lang=='FR' else 1]
def status_label(value,lang):return STATUS.get(value,(value,value))[0 if lang=='FR' else 1]
