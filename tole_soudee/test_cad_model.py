import unittest,copy,math,json
from pathlib import Path
import cadquery as cq
from cad_model import load_parameters,derived,build,example_indications,indication_shapes,rotation_xyz,ROOT
import numpy as np

class PlateGeometryTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.p=load_parameters();cls.parts,cls.d=build(cls.p,finish=False)
 def test_approved_dimensions_and_valid_solids(self):
  self.assertEqual(len(self.parts),9)
  self.assertAlmostEqual(self.d['opening'],9.75)
  self.assertAlmostEqual(self.d['land_high']-self.d['land_low'],1.25)
  self.assertAlmostEqual(self.d['cap_radius'],17.45)
  for shape in self.parts.values():self.assertTrue(shape.isValid());self.assertEqual(len(shape.Solids()),1)
 def test_plate_partition_preserves_volume_without_overlaps(self):
  shapes=[s for name,s in self.parts.items() if not name.startswith('BOURRELET')]
  self.assertAlmostEqual(sum(s.Volume() for s in shapes),245*250*10,places=6)
  for i,a in enumerate(shapes):
   for b in shapes[i+1:]:self.assertLess(abs(a.intersect(b).Volume()),1e-6)
 def test_symmetric_circular_caps_match_analytic_segment(self):
  R=self.d['cap_radius'];h=self.p['caps']['height'];a=self.p['caps']['width']/2
  expected=(R*R*math.acos((R-h)/R)-(R-h)*a)*245
  for key in ['BOURRELET_SUPERIEUR','BOURRELET_INFERIEUR']:
   self.assertAlmostEqual(self.parts[key].Volume(),expected,places=5)
  self.assertAlmostEqual(self.parts['BOURRELET_SUPERIEUR'].BoundingBox().zmax,12.5,places=5)
  self.assertAlmostEqual(self.parts['BOURRELET_INFERIEUR'].BoundingBox().zmin,-2.5,places=5)
 def test_four_bevel_faces_are_45_degrees(self):
  normals=[]
  for face in self.parts['METAL_FONDU_X'].Faces():
   n=face.normalAt()
   if abs(n.x)<1e-8 and abs(n.y)>.1 and abs(n.z)>.1:normals.append(n)
  self.assertEqual(len(normals),4)
  for n in normals:self.assertAlmostEqual(math.degrees(math.atan2(abs(n.z),abs(n.y))),45.,places=7)
 def test_land_variants_rebuild_and_invalid_gap_rejected(self):
  for land in [1.,1.5]:
   p=copy.deepcopy(self.p);p['joint']['land']=land
   parts,d=build(p,finish=False)
   self.assertAlmostEqual(d['opening'],1+10-land)
   self.assertTrue(all(s.isValid() for s in parts.values()))
  p=copy.deepcopy(self.p);p['joint']['gap']=30
  with self.assertRaises(ValueError):derived(p)
 def test_reference_flaws_match_sizes_and_actual_bevel_planes(self):
  rows=example_indications(self.p,self.d);shapes=indication_shapes(rows)
  for row in rows:
   shape=shapes[row['id']]
   if row['diameter_mm']:
    self.assertAlmostEqual(shape.Volume(),4*math.pi*(.25**3)/3,places=8)
   else:
    R=rotation_xyz(row['rx_deg'],row['ry_deg'],row['rz_deg']);center=np.array([row[k] for k in ('x_mm','y_mm','z_mm')]);points=np.array([R.T@(np.array(v.toTuple())-center) for v in shape.Vertices()])
    self.assertAlmostEqual(np.ptp(points[:,0]),row['length_mm'],places=6)
    self.assertAlmostEqual(np.ptp(points[:,1]),row['width_mm'],places=6)
    self.assertLess(np.max(abs(points[:,2])),1e-8)
    self.assertEqual(len(shape.Solids()),0) # No fabricated air opening.
   if row['id'].startswith('MF'):
    sign=-1 if row['id']=='MF1' else 1
    for v in shape.Vertices():
     x,y,z=v.toTuple();expected=125+sign*(.5+z-self.d['land_high'])
     self.assertAlmostEqual(y,expected,places=7)
 def test_step_round_trip_and_finish_geometry(self):
  file=ROOT/'cad_exports/TOLE_X_245_250_10_ASSEMBLAGE.step'
  imported=cq.importers.importStep(str(file)).val()
  self.assertEqual(len(imported.Solids()),9)
  english=cq.importers.importStep(str(ROOT/'cad_exports/WELDED_PLATE_X_245_250_10_ASSEMBLY_EN.step')).val()
  self.assertEqual(len(english.Solids()),9)
  self.assertAlmostEqual(english.Volume(),imported.Volume(),places=5)
  self.assertTrue(imported.isValid())
  for s in imported.Solids():self.assertTrue(s.isValid())
  expected_total=sum(s.Volume() for s in self.parts.values())
  self.assertGreater(expected_total-imported.Volume(),0)
  self.assertLess(expected_total-imported.Volume(),.01*sum(self.parts[n].Volume() for n in ['BOURRELET_SUPERIEUR','BOURRELET_INFERIEUR']))
  self.assertAlmostEqual(imported.BoundingBox().xlen,245,places=4)
  self.assertAlmostEqual(imported.BoundingBox().ylen,250,places=4)
  self.assertAlmostEqual(imported.BoundingBox().zlen,15,places=4)

if __name__=='__main__':unittest.main()
