from typing import List
from .csv_reader import CSVReader


class CSVDrugReader(CSVReader):

    @property
    def header(self) -> List[str]:
        return [
            "atccode",
            "drug",
        ]