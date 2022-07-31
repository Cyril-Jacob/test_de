from typing import List
from .csv_reader import CSVReader


class CSVPubReader(CSVReader):

    @property
    def header(self) -> List[str]:
        return [
            "id",
            "title",
            "date",
            "journal",
        ]
        


