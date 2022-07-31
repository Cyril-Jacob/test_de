import re
from datetime import datetime
from typing import Tuple, overload
from .publication import Publication 

class ClinicalTrials(Publication):
    """class implementing Clinical trials publications 

    Args:
        Publication (_type_): Abstract class representing publications
    """

    def __init__(self, id:str, title: str, date: str, journal: str) -> None:
        """Initialize a clinical trial publication

        Args:
            id (str): unique identifier of a clinical trial in the form of NCT04189588
            title (str): scientific title of the clinical trial
            date (str): publication date in the form 01 January 2020
            journal (str): journal title it belongs to
        """
        id, title, date, journal = ClinicalTrials.clean_row(id, title, date, journal)
        ClinicalTrials.validate_row(id, title, date, journal)
        super().__init__(id, title, datetime.strptime(date,"%d %B %Y"), journal)
    
    @classmethod
    def validate_row(cls, id:str, title: str, date: str, journal: str) -> None:
        """Check validity of clinical trials rows

        Args:
            id (str): unique identifier
            title (str): scientific title
            date (str): publication date
            journal (str): journal title it belongs to

        Raises:
            Publication.InvalidRowError: wrong publication id. It should be in the form of NCT\d{8}
            Publication.InvalidRowError: missing mandatory title or journal parameter
        """
        r = re.compile(r'NCT\d{8}')
        if r.match(id) is None:
            raise Publication.InvalidRowError(f"id should be of the form 'NCT\d{8}' but is '{id}'")

        if not title.split() or not journal.split():
            raise Publication.InvalidRowError("title or journal must not be empty")
        
    @classmethod
    def clean_row(cls, id:str, title: str, date: str, journal: str) -> Tuple[str,str,str,str]: # type: ignore[override]
        """ Remove wrong pattern in clinical trials rows such as not encoded characters

        Args:
            id (str): unique identifier
            title (str): scientific title
            date (str): publication date
            journal (str): journal title it belongs to

        Returns:
            Tuple[str,str,str,str]: cleaned row
        """
        unicode_character_to_clean = ('\\xc3\\x28', '\\xc3\\xb1')
        for u in unicode_character_to_clean:
            title = title.replace(u,'')
            journal = journal.replace(u,'')
        return (id, title, date, journal)


    def __repr__(self):
        return (
            f"{self.__class__.__name__} ("
            f"scientific_title='{self.title}', "
            f"journal_title='{self.journal}', "
            f"date='{self.date}', "
            f"id='{self.id}'"
            f")"
        )


if __name__ == "__main__":

    ClinicalTrials.validate_row("NCT12345678","  3   ","","3 ")

    d = {'id':'NCT04188184','title': 'Preemptive Infiltration With Betamethasone and Ropivacaine for Postoperative Pain in Laminoplasty or \\xc3\\xb1 Laminectomy','date':"27 April 2020",'journal':"Hôpitaux Universitaires de Genève"}
    print(ClinicalTrials.clean_row(**d))