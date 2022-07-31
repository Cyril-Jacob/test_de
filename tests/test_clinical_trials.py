

import unittest
from drug_journal.pub.publication import Publication

from drug_journal.pub.clinical_trials import ClinicalTrials

'''
title error row with extra not encoded characters
'''

clinical_row = ("NCT04188184"," ","27 April 2020","Journal of emergency nursing\\xc3\\x28")

class TestClinicalTrial(unittest.TestCase):

    def test_clean_row(self):
        id, title, date, journal = ClinicalTrials.clean_row(*clinical_row)
        self.assertEqual(journal, "Journal of emergency nursing")

    def test_validate_row(self):
        #id, title, date, journal = ClinicalTrials.validate_row(*clinical_row)
        self.assertRaisesRegex(Publication.InvalidRowError, "title or journal must not be empty", ClinicalTrials.validate_row, *clinical_row)

if __name__ == '__main__':
    unittest.main()