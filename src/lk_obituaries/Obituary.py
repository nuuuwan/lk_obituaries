from dataclasses import dataclass
from functools import cached_property


@dataclass
class Obituary:
    newspaper_id: str
    ut: int
    date_str_file: str
    i: int
    raw_text: str

    @cached_property
    def dict(self):
        return dict(
            newspaper_id=self.newspaper_id,
            ut=self.ut,
            date_str_file=self.date_str_file,
            i=self.i,
            raw_text=self.raw_text,
        )

    def __lt__(self, other):
        if self.ut != other.ut:
            return self.ut < other.ut

        if self.newspaper_id != other.newspaper_id:
            return self.newspaper_id < other.newspaper_id

        if self.i != other.i:
            return self.i < other.i

        return 0
