from pathlib import Path
from typing import Iterator, List
import csv
import abc

class CSVReader(abc.ABC):
    """ Abstract class to help build common features between different CSV format reader """
    

    @abc.abstractproperty
    def header(self) -> List[str]:
        """header fields container

        Returns:
            List[str]: a list containing CSV header fields
        """
        ...

    def __init__(self, source: Path) -> None:
        self.source = source


    def data_iter(self) -> Iterator[dict[str, str]]:
        with self.source.open(encoding="utf-8") as source_file:
            reader = csv.DictReader(source_file, self.header)
            yield from reader
        