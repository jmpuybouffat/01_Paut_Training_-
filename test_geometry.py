import unittest
import numpy as np
from geometry import preparation, validate_dimensions

class GeometryTests(unittest.TestCase):
 def test_invalid_dimensions(self):
  self.assertTrue(validate_dimensions(100,60,40,5,0,2))
  self.assertTrue(validate_dimensions(400,20,160,90,0,2))
  self.assertFalse(validate_dimensions(400,20,160,12,0,2))
 def test_preparation_cylinders_and_gap(self):
  a=np.deg2rad(63); axis=np.array([np.sin(a),0,np.cos(a)]); basis=np.array([np.cos(a),0,-np.sin(a)])
  th=np.linspace(0,2*np.pi,121)
  face,cap=preparation(th,180,200,80,0,axis,basis,np.array([0,1,0]),35,2,2,3)
  self.assertTrue(np.isfinite(face).all())
  np.testing.assert_allclose(np.linalg.norm(face[0,:,:2],axis=1),180,atol=1e-8)
  np.testing.assert_allclose(np.linalg.norm(face[-1,:,:2],axis=1),200,atol=1e-8)
  perp=face[0]-np.outer(face[0]@axis,axis)
  np.testing.assert_allclose(np.linalg.norm(perp,axis=1),82,atol=1e-8)
  self.assertGreater(np.max(np.linalg.norm(cap[...,:2],axis=-1)),202)

if __name__=='__main__': unittest.main()
