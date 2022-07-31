

import unittest

from drug_journal.drug import Drug


class TestDrug(unittest.TestCase):

    def test_add_pubmed(self):
        Drug.add_pubmed("TETRACYCLINE".lower(), "dnodieozf", "2020-05-12")
   
        self.assertEqual(len(Drug.drug_dict['tetracycline'].get('pubmed')), 1)


    def test_get_journal_with_higher_drugs(self):
        Drug.add_pubmed("TETRACYCLINE".lower(), "dnodieozf", "2020-05-12")
        Drug.add_journal("TETRACYCLINE1".lower(), "journal1", "2020-05-12")
        Drug.add_journal("TETRACYCLINE2".lower(), "journal1", "2020-05-12")
        Drug.add_journal("TETRACYCLINE1".lower(), "journal2", "2020-05-12")
        Drug.add_journal("TETRACYCLINE2".lower(), "journal3", "2020-05-12")

        self.assertEqual(Drug.get_journal_with_higher_drugs(), (2,"journal1"))

if __name__ == '__main__':
    unittest.main()