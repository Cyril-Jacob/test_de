import unittest
from pathlib import Path

from drug_journal.reader.csv_drug_reader import CSVDrugReader


class TestCSVDrugReader(unittest.TestCase):

    def test_data_iter(self):
        
        drug_row = list(CSVDrugReader(Path('data/input/drugs.csv')).data_iter())
        
        self.assertEqual(len(drug_row), 8)
