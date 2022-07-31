import unittest
from pathlib import Path

from drug_journal.reader.json_pub_reader import JSONPubReader

class TestJsonPubReader(unittest.TestCase):

    def test_json_pub_reader(self):
        json_pub_row =  list(JSONPubReader(Path("data/input/pubmed.json")).data_iter())
   
        self.assertEqual(len(json_pub_row), 5)
