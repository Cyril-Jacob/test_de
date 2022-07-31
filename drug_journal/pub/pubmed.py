from datetime import datetime
from typing import Tuple, cast
from .publication import Publication

class Pubmed(Publication):
    """class implementing medical publications coming from the search engine PubMed

    Args:
        Publication (_type_): Abstract class representing publications 
    """

    def __init__(self, id:str, title: str, date: str, journal: str) -> None:
        """Initialize a PubMed publication

        Args:
            id (str): unique identifier of a pubmed in the form of 12
            title (str): article title
            date (str): publication date in the form of 01/01/2020
            journal (str): journal title it belongs to
        """
        id, title, date, journal = Pubmed.clean_row(id, title, date, journal)
        Pubmed.validate_row(id, title, date, journal)
        super().__init__(id, title, datetime.strptime(date,"%d/%m/%Y"), journal)
    
    @classmethod
    def validate_row(self, id:str, title: str, date: str, journal: str) -> None:
        """ Check validity of PubMed rows

        Args:
            id (str): unique identifier of a pubmed in the form of 12
            title (str): article title
            date (str): publication date in the form of 01/01/2020
            journal (str): journal title it belongs to

        Raises:
            Publication.InvalidRowError: id should be positive integer
        """
        if not id.isdigit():
            raise Publication.InvalidRowError("id should be a positive integer")

    @classmethod
    def clean_row(self, id:str, title: str, date: str, journal: str) -> Tuple[str,str,str,str]: # type: ignore[override]
        """ Clean PubMed rows such as enforcing id to be its string representation

       Args:
            id (str): unique identifier of a pubmed in the form of 12
            title (str): article title
            date (str): publication date in the form of 01/01/2020
            journal (str): journal title it belongs to

        Returns:
            Tuple[str,str,str,str]: cleaned row
        """
        return (str(id), title, date, journal)

    def __repr__(self):
        return (
            f"{self.__class__.__name__} ("
            f"title='{self.title}', "
            f"journal_title='{self.journal}', "
            f"date='{self.date}', "
            f"id='{self.id}'"
            f")"
        )

if __name__ == "__main__":
    pass
    