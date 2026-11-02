"""Actual preset callback and editable surface-normal parameter."""
import unittest
from streamlit.testing.v1 import AppTest

class ScatteringPresetTests(unittest.TestCase):
 def test_witness_loads_geometry_scan_and_single_surface(self):
  app=AppTest.from_file('app.py').run(timeout=60)
  next(b for b in app.button if b.key=='load_backscatter_witness').click().run(timeout=60)
  self.assertFalse(app.exception)
  self.assertEqual(app.session_state['selection_control_training_scenario'],'PIECE_PERSONNALISEE')
  rows=app.session_state['canonical_table_project_PIECE_PERSONNALISEE']
  self.assertEqual([r['id'] for r in rows if r['enabled']],['MF1'])
  self.assertEqual(rows[0]['normal_tilt_deg'],45.)
  self.assertEqual(rows[0]['depth_mm'],10.)
  self.assertEqual(app.session_state['control_scan_a0'],-50.)
  self.assertEqual(app.session_state['control_scan_z0'],-100.)
  self.assertEqual(app.session_state['control_vs'],3240)
  app.sidebar.radio[0].set_value('EN').run(timeout=60)
  self.assertFalse(app.exception)
  self.assertEqual(app.session_state['selection_control_training_scenario'],'PIECE_PERSONNALISEE')
  self.assertEqual(app.session_state['canonical_table_project_PIECE_PERSONNALISEE'][0]['normal_tilt_deg'],45.)


 def test_protocol_is_english_when_en_selected(self):
  app=AppTest.from_file('app.py').run(timeout=60)
  app.sidebar.radio[0].set_value('EN').run(timeout=60)
  self.assertFalse(app.exception)
  texts=[m.value for m in app.markdown]
  protocol=next(t for t in texts if '# User test protocol' in t)
  self.assertIn('Test 9 — computed backscattered field',protocol)
  self.assertNotIn('Préparation commune',protocol)
  self.assertNotIn('Protocole utilisateur',protocol)
  app.sidebar.radio[0].set_value('FR').run(timeout=60)
  self.assertTrue(any('# Protocole utilisateur' in m.value for m in app.markdown))

if __name__=='__main__':unittest.main()
