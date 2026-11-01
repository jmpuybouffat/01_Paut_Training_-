import unittest
from i18n import VALUES,translate_rows,column_label,display_value
from libraries import gesture_demo_indications

class TranslationTests(unittest.TestCase):
 def test_values_roundtrip(self):
  for column,values in VALUES.items():
   for key in values:
    for lang in ['FR','EN']:
     row=translate_rows([{column:key}],lang)
     self.assertEqual(translate_rows(row,lang,canonical=True)[0][column],key)
 def test_project_english_and_numbers(self):
  original=gesture_demo_indications(20)
  shown=translate_rows(original,'EN')
  self.assertEqual(shown[0]['type'],'Lack of fusion')
  self.assertTrue(shown[0]['location'].startswith('Artificial main-wall'))
  self.assertEqual(shown[0]['depth_mm'],original[0]['depth_mm'])
  self.assertEqual(translate_rows(shown,'EN',canonical=True),original)
 def test_user_text_not_rewritten(self):
  row={'location':'Fabien specimen A, weld side 2','length_mm':6.}
  self.assertEqual(translate_rows([row],'EN')[0],row)
  self.assertEqual(column_label('length_mm','EN'),'Length (mm)')
  self.assertEqual(display_value('access','TO_ASSESS','FR'),'Évaluer l’encombrement')

if __name__=='__main__':unittest.main()
