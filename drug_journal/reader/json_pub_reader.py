from pathlib import Path
from typing import Iterator
from typing import Union
import json5 #type: ignore [import]
import logging


class JSONPubReader:

    key_value = [
        "id",
        "title",
        "date",
        "journal",
    ]

    def __init__(self, source: Path) -> None:
        self.source = source

    
    def data_iter(self) -> Iterator[dict[str, str]]:
        with self.source.open(encoding="utf-8") as source_file:
            try:
                # TODO update object_hook function in case we have clinical_trials in JSON to replace scientific_title with title 
                reader = json5.load(source_file) 
                yield from reader
            except json5.JSONDecodeError as ex:
                 logging.getLogger(__name__).error(f"Json decoding failed: {ex}\n")