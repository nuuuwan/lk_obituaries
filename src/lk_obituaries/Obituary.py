import os
from dataclasses import dataclass

from utils import JSONFile, Log, Time, TimeFormat

log = Log('Obituary')


@dataclass
class Obituary:
    DIR_DATA = 'data'

    newspaper_id: str
    ut: int
    i: int
    raw_text: str

    def to_dict(self) -> dict:
        return dict(
            ut=self.ut,
            date_str=self.date_str,
            newspaper_id=self.newspaper_id,
            i=self.i,
            raw_text=self.raw_text,
        )

    @staticmethod
    def from_dict(d) -> 'Obituary':
        return Obituary(
            ut=int(d['ut']),
            newspaper_id=d['newspaper_id'],
            i=int(d['i']),
            raw_text=d['raw_text'],
        )

    @property
    def date_str(self) -> str:
        return TimeFormat('%Y-%m-%d').stringify(Time(self.ut))

    @property
    def dir_data(self) -> str:
        dir_data = os.path.join(
            Obituary.DIR_DATA, self.date_str, self.newspaper_id
        )
        if not os.path.exists(dir_data):
            os.makedirs(dir_data)
        return dir_data

    @property
    def raw_text_start(self) -> str:
        return self.raw_text.strip().partition(' ')[0].lower()

    @property
    def file_only(self) -> str:
        return f'{self.date_str}-{self.newspaper_id}'+f'-{self.i}-{self.raw_text_start}.json'

    @property
    def data_path(self) -> str:
        return os.path.join(self.dir_data, f'{self.file_only}')

    def __lt__(self, other):
        if self.ut != other.ut:
            return self.ut < other.ut

        if self.newspaper_id != other.newspaper_id:
            return self.newspaper_id < other.newspaper_id

        if self.i != other.i:
            return self.i < other.i

        return 0

    @staticmethod
    def list_all() -> list['Obituary']:
        obituary_list = []
        for date_str in os.listdir(Obituary.DIR_DATA):
            dir_data_for_date = os.path.join(Obituary.DIR_DATA, date_str)
            for newspaper_id in os.listdir(dir_data_for_date):
                dir_data_for_newspaper = os.path.join(
                    dir_data_for_date, newspaper_id
                )
                for file_only in os.listdir(dir_data_for_newspaper):
                    file_path = os.path.join(
                        dir_data_for_newspaper, file_only
                    )
                    data = JSONFile(file_path).read()
                    obituary = Obituary.from_dict(data)
                    obituary_list.append(obituary)
        obituary_list.sort(reverse=True)
        return obituary_list

    @staticmethod
    def list_for_newspaper(newspaper_id: str) -> list['Obituary']:
        return [
            obituary
            for obituary in Obituary.list_all()
            if obituary.newspaper_id == newspaper_id
        ]

    @staticmethod
    def idx() -> dict[str, list['Obituary']]:
        idx = {}
        for obituary in Obituary.list_all():
            date_str = obituary.date_str_file
            if date_str not in idx:
                idx[date_str] = []
            idx[date_str].append(obituary)
        return idx

    def write(self):
        if os.path.exists(self.data_path):
            log.warning(f'🟡 Already crawled {self.data_path}')
            return

        JSONFile(self.data_path).write(self.to_dict())
        log.debug(f'Wrote {self.data_path}')
