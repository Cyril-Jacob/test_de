

import unittest
from drug_journal.pub.publication import Publication

from drug_journal.pub.pubmed import Pubmed

'''
First row has an id as int instead of string
Second row has a missing id
'''
pubmed_lst=  [{
    "id": 9,
    "title": "Gold nanoparticles synthesized from Euphorbia fischeriana root by green route method alleviates the isoprenaline hydrochloride induced myocardial infarction in rats.",
    "date": "01/01/2020",
    "journal": "Journal of photochemistry and photobiology. B, Biology"
  },
  {
    "id": " ",
    "title": "Gold nanoparticles synthesized from Euphorbia fischeriana root by green route method alleviates the isoprenaline hydrochloride induced myocardial infarction in rats.",
    "date": "01/01/2020",
    "journal": "Journal of photochemistry and photobiology. B, Biology"
  }
  ]

class TestPubmed(unittest.TestCase):

    def test_clean_row(self):
        id, title, date, journal = Pubmed.clean_row(**pubmed_lst[0])
        self.assertEqual(id, "9")

    def test_validate_row(self):
        self.assertRaisesRegex(Publication.InvalidRowError, "id should be a positive integer" ,Pubmed.validate_row, **pubmed_lst[1])

if __name__ == '__main__':
    unittest.main()