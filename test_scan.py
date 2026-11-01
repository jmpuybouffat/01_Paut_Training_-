import unittest
from scan import plan_scan,beam_segment

class ScanTests(unittest.TestCase):
 def zone(self,access='TO_ASSESS'):
  return dict(access=access,available_length_mm=100,available_width_mm=100,probe_length_mm=10,probe_width_mm=10,travel_mm=10,margin_mm=1,azimuth_start_deg=350,azimuth_end_deg=10,z_start_mm=-20,z_end_mm=20)
 def test_wrap_and_block(self):
  rows=plan_scan(200,800,-10,10,0,0,10,[self.zone('INACCESSIBLE')])
  self.assertTrue(all(r['status']=='BLOCKED' for r in rows))
 def test_unknown_does_not_count_as_scanned(self):
  self.assertEqual(plan_scan(200,800,0,0,0,0,10,[])[0]['status'],'UNASSESSED')
 def test_accessible_plan(self):
  self.assertEqual(plan_scan(200,800,0,0,0,0,10,[self.zone()])[0]['status'],'PLANNED')
 def test_unlocated_exclusion_blocks(self):
  z=self.zone('INACCESSIBLE');z['z_start_mm']=None
  self.assertEqual(plan_scan(200,800,90,90,0,0,10,[z])[0]['status'],'BLOCKED')
 def test_limits(self):
  with self.assertRaises(ValueError): plan_scan(200,800,0,360,-400,400,.01,[])
 def test_axial_beam(self):
  p=beam_segment([200,0,0],200,20,45,0)
  self.assertAlmostEqual(p[0],180);self.assertAlmostEqual(p[2],20)
if __name__=='__main__': unittest.main()
