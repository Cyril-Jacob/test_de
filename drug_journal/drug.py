from typing import Dict
from typing import List
import json


class Drug():
    """ class representing the drug dependency graph with publications and journals"""
    

    drug_dict: Dict[str,Dict[str,List[Dict[str,str]]]] = {}
    """ The Python structure representing the graph 
    
    e.g.

    {
    "betamethasone": {
        "journal": [
            {
                "date": "01/01/20",
                "title": "The journal of maternal-fetal & neonatal medicine"
            }
        ],
        "pubmed": [
            {
                "date": xxx
                "title": xxx
            }
        ],
        "scientific": [
            {
                "date": xxx
                "title": xxx
            }
        ]
    },
    ...
    """
    
    @classmethod
    def get_or_create_drug(cls, drug: str) -> Dict[str,List[Dict[str,str]]]:
        if drug not in  Drug.drug_dict:
            Drug.drug_dict[drug] = {"pubmed": [], "scientific":[], "journal":[]}
        return Drug.drug_dict[drug]

    @classmethod
    def add_pubmed(cls,drug:str, title:str,date:str) -> None:
        d = cls.get_or_create_drug(drug)
        d["pubmed"].append({"title":title,"date":date})
    
    @classmethod
    def add_scientific(cls,drug:str, title:str,date:str) -> None:
        d = cls.get_or_create_drug(drug)
        d["scientific"].append({"title":title,"date":date})
    
    @classmethod
    def add_journal(cls,drug:str, title:str,date:str) -> None:
        d = cls.get_or_create_drug(drug)
        d["journal"].append({"title":title,"date":date})

    @classmethod
    def get_json(cls) -> str:
        """Get Json formatted drug dependency graph with journals and publications

        Returns:
            str: JSON string
        """
        return json.dumps(cls.drug_dict, ensure_ascii=False, sort_keys=True, indent=4)

    @classmethod
    def get_journal_with_higher_drugs(cls) -> tuple[int,str]:
        """Browse Python structure defined in drug_dict in order to build a list of journals with the number of different drugs mentioned in them.

        Returns:
            tuple[int,str]: (number of different drugs occuring in the journal, journal title)
        """
        journal_dict: Dict[str,set[str]] = {}
        for d,v in cls.drug_dict.items():
            for j_dict in v['journal']:
                j = j_dict['title']
                if j not in journal_dict:
                    journal_dict[j] = set({d})
                else:
                    journal_dict[j].add(d)
        journal_drug_len_lst = [(len(journal_dict[k]),k) for k in journal_dict]
        return max(journal_drug_len_lst)

if __name__ == "__main__":
    pass
    
