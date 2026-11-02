"""Exercise actual editor state across FR/EN changes without resetting geometry."""
import unittest
from streamlit.testing.v1 import AppTest

class LanguageStateTests(unittest.TestCase):
 def test_editor_and_geometry_preserved(self):
  app=AppTest.from_file('app.py').run(timeout=45)
  self.assertFalse(app.exception)
  key='editor_project_DEMO_GESTE_PAROI_FR'
  app.session_state[key]={'edited_rows':{0:{'length_mm':7.5}},'added_rows':[],'deleted_rows':[]}
  app.run(timeout=45)
  self.assertFalse(app.exception)
  store='canonical_table_project_DEMO_GESTE_PAROI'
  self.assertEqual(app.session_state[store][0]['length_mm'],7.5)
  next(x for x in app.sidebar.slider if x.key=='control_D1').set_value(450.).run(timeout=45)
  app.sidebar.radio[0].set_value('EN').run(timeout=45)
  self.assertFalse(app.exception)
  self.assertEqual(next(x for x in app.sidebar.selectbox if x.key=='control_workflow_EN').options[0],'Training')
  self.assertEqual(next(x for x in app.sidebar.selectbox if x.key=='control_training_scenario_EN').options[0],'Main-wall scan demo')
  self.assertEqual(next(x for x in app.sidebar.selectbox if x.key=='control_mouse_mode_EN').options[0],'Orbit')
  self.assertEqual(app.session_state[store][0]['length_mm'],7.5)
  self.assertEqual(next(x for x in app.sidebar.slider if x.key=='control_D1').value,450.)
  table=next(x.value for x in app.dataframe if 'type' in x.value.columns)
  self.assertEqual(table.iloc[0]['type'],'Lack of fusion')
  self.assertTrue(table.iloc[0]['location'].startswith('Artificial main-wall'))
  app.sidebar.radio[0].set_value('FR').run(timeout=45)
  self.assertFalse(app.exception)
  self.assertEqual(app.session_state[store][0]['length_mm'],7.5)
  table=next(x.value for x in app.dataframe if 'type' in x.value.columns)
  self.assertEqual(table.iloc[0]['type'],'Collage / manque de fusion')

 def test_scan_exclusion_and_added_rows_preserved(self):
  app=AppTest.from_file('app.py').run(timeout=45)
  app.session_state['editor_scan_access_FR']={'edited_rows':{0:{'access':'Inaccessible','azimuth_start_deg':-10.,'azimuth_end_deg':10.,'z_start_mm':0.,'z_end_mm':30.}},'added_rows':[{'zone':'Extra','access':'Non évalué'}],'deleted_rows':[]}
  app.run(timeout=45)
  self.assertFalse(app.exception)
  self.assertEqual(len(app.session_state['canonical_table_scan_access']),2)
  app.run(timeout=45)
  self.assertEqual(len(app.session_state['canonical_table_scan_access']),2)
  for lang in ['EN','FR']:
   app.sidebar.radio[0].set_value(lang).run(timeout=45)
   self.assertFalse(app.exception)
   rows=app.session_state['canonical_table_scan_access']
   self.assertEqual(len(rows),2)
   self.assertEqual(rows[0]['access'],'INACCESSIBLE')
   self.assertEqual(rows[0]['z_end_mm'],30.)
   self.assertEqual(rows[1]['access'],'UNASSESSED')

if __name__=='__main__':unittest.main()
