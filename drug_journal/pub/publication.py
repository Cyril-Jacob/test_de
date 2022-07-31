import abc
from datetime import datetime
from sre_constants import INFO
from turtle import title
from typing import Dict, Iterable, Iterator, overload
import logging

class Publication(abc.ABC):
    """ Abstract factory class that represents a publication 

    Args:
        abc (_type_): _description_

    Raises:
        Publication.InvalidRowError: Specific error raised when an issue in a row that cannot be recovered is spotted

    Returns:
        _type_: an instance representing a specific publication

    Yields:
        _type_: a cleaned and validated row defining a publication
    """

    class InvalidRowError(ValueError):
        pass

    pub_dict: Dict[str,'Publication'] = {}

    @abc.abstractmethod
    def __init__(self, id:str, title: str, date: datetime, journal: str) -> None:
        self.id, self.title, self.date, self.journal = Publication.clean_row(id, title, date, journal)
        if self.id not in Publication.pub_dict:
            Publication.pub_dict[self.id] = self
        else:
            logging.getLogger(__name__).info(f"Duplicates: Trying to add an already added publication {self!r}")
    
    def get_dict(self) -> dict[str,str]:
        return dict(id=self.id, title=self.title, date=self.date.strftime("%d/%m/%y"), journal=self.journal)

    @staticmethod
    def is_drug_in_title(drug:str, title:str) -> bool:
        """Method used to determine if a specific drug is mentioned in the tile of a publication

        Args:
            drug (str): drug name
            title (str): publication title

        Returns:
            bool: True if the drug is mentioned Otherwise False
        """
        return title.__contains__(drug)

    @classmethod
    def clean_row(cls, id:str, title: str, date: datetime, journal: str) -> tuple[str,str,datetime,str]:
        return (id, title.lower(), date, journal)



    @classmethod
    def from_dict(cls, row: dict[str, str]) -> 'Publication':
        try:
            return cls(**row) #type: ignore[arg-type]
        except (ValueError, TypeError) as ex:
            raise Publication.InvalidRowError(f"invalid {row!r} - {ex}")

    @classmethod
    def load(cls, raw_data_iter: Iterable[dict[str,str]]) -> Iterator[dict[str,str]]:
        for n, row in enumerate(raw_data_iter):
            try:
                yield cls.from_dict(row).get_dict()
            except Publication.InvalidRowError as ex :
                logging.getLogger(__name__).error(f"Row {n+1} skipped: {ex}\n",)

    @abc.abstractmethod
    def __repr__(self, ) -> str:
        ...