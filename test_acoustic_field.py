import unittest
import numpy as np
from acoustic_field import scalar_aperture_cut

class ScalarFieldTests(unittest.TestCase):
 def test_symmetry_and_normalization(self):
  result=scalar_aperture_cut(4,3240,ns=35,nt=25)
  field=np.asarray(result['amplitude_db'])
  np.testing.assert_allclose(field,field[:,::-1],atol=.03)
  self.assertAlmostEqual(field.max(),0,places=2)
  self.assertTrue(np.isfinite(field).all())
 def test_frequency_changes_pattern(self):
  a=scalar_aperture_cut(4,3240,ns=30,nt=25)
  b=scalar_aperture_cut(5,3240,ns=30,nt=25)
  self.assertGreater(np.max(np.abs(np.array(a['amplitude_db'])-b['amplitude_db'])),1.)
 def test_far_field_rectangular_directivity(self):
  result=scalar_aperture_cut(4,3240,s_max_mm=500,transverse_max_mm=80,ns=7,nt=33)
  field=np.array(result['amplitude_db'])[-1]
  t=np.array(result['transverse_mm']);s=500.;wavelength=.81
  index=int(np.argmin(abs(t-25)))
  distance=np.hypot(s,t[index])
  expected=20*np.log10(abs(np.sinc(8*t[index]/distance/wavelength))*s/distance)
  self.assertAlmostEqual(field[index]-field[len(t)//2],expected,delta=.3)
 def test_three_dimensional_volume(self):
  result=scalar_aperture_cut(2,3240,ns=20,nt=15,include_volume=True)
  volume=np.array(result['volume']['amplitude_db'])
  self.assertEqual(volume.shape,(65,25,25))
  np.testing.assert_allclose(volume,volume[:,::-1,:],atol=.03)
  np.testing.assert_allclose(volume,volume[:,:,::-1],atol=.03)
  self.assertLessEqual(volume.max(),.001)
 def test_invalid_source(self):
  with self.assertRaises(ValueError):scalar_aperture_cut(0,3240)

if __name__=='__main__':unittest.main()
