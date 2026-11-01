import unittest
import numpy as np
from joint_profiles import faceted_joint_profiles

class ProfileTests(unittest.TestCase):
 def make(self,seed=17):return faceted_joint_profiles(200,180,80,63,0,800,2,2,35,3,seed=seed)
 def test_repeatability_and_seed(self):
  a=self.make();b=self.make();c=self.make(18)
  self.assertEqual(a,b)
  self.assertNotEqual(a['meshes']['cap']['vertices_mm'],c['meshes']['cap']['vertices_mm'])
 def test_closed_seam_and_normals(self):
  p=self.make()
  for name in ['root','cap']:
   vertices=np.array(p['meshes'][name]['vertices_mm'])
   np.testing.assert_allclose(vertices[:5],vertices[-5:],atol=1e-8)
   np.testing.assert_allclose(np.linalg.norm(p['references'][name]['normals'],axis=1),1.,atol=1e-8)
   self.assertFalse(p['meshes'][name]['measured'])

if __name__=='__main__':unittest.main()
