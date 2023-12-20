import os
from functools import cached_property

from utils import SECONDS_IN, JSONFile, Log, Time, TimeFormat

from lk_obituaries.Obituary import Obituary

log = Log('NewsPaper')


class NewsPaper:
    TIME_FORMAT_FILE = TimeFormat('%Y-%m-%d')

    @classmethod
    def get_name(cls) -> str:
        raise NotImplementedError

    @classmethod
    def get_url(cls) -> str:
        raise NotImplementedError

    @classmethod
    def get_id(cls) -> str:
        return cls.get_name().replace(' ', '-').lower()

    @classmethod
    def get_dir_data(cls) -> str:
        dir_data = os.path.join('data', cls.get_id())
        if not os.path.exists(dir_data):
            os.makedirs(dir_data)
        return dir_data

    def __init__(self, delta_days: int):
        self.delta_days = delta_days

    @cached_property
    def time(self) -> Time:
        ut = Time.now().ut - self.delta_days * SECONDS_IN.DAY
        ut = int(ut / SECONDS_IN.DAY) * SECONDS_IN.DAY
        return Time(ut)

    @cached_property
    def obituary_list(self) -> list[Obituary]:
        raise NotImplementedError

    @cached_property
    def date_str_file(self) -> str:
        return NewsPaper.TIME_FORMAT_FILE.stringify(self.time)

    @cached_property
    def data_path(self) -> str:
        return os.path.join(
            self.__class__.get_dir_data(), f'{self.date_str_file}.json'
        )

    def crawl(self):
        log.info(f'🤖 Crawling {self.date_str_file}')
        obituary_list = self.obituary_list
        data_list = [obituary.dict for obituary in obituary_list]
        JSONFile(self.data_path).write(data_list)
        log.info(f'✅ Wrote {len(obituary_list)} records to {self.data_path}')

    @classmethod
    def crawl_today(cls):
        cls(0).crawl()

    @classmethod
    def crawl_range(cls, min_delta_days: int, max_delta_days: int):
        for delta_days in range(min_delta_days, max_delta_days + 1):
            log.debug(f'Crawling {delta_days}/{max_delta_days}')
            cls(delta_days).crawl()

    @classmethod
    def get_obituary_list(cls) -> list[Obituary]:
        dir_data = cls.get_dir_data()
        all_obituary_list = []
        for file_only in os.listdir(dir_data):
            file_path = os.path.join(dir_data, file_only)
            data_list = JSONFile(file_path).read()
            obituary_list = [Obituary(**data) for data in data_list]
            all_obituary_list.extend(obituary_list)
        log.info(f'Loaded {len(all_obituary_list)} records from {dir_data}')
        all_obituary_list.sort(reverse=True)
        return all_obituary_list

    @classmethod
    def get_obituary_list_by_date(cls) -> dict[str, list[Obituary]]:
        idx = {}
        for obituary in cls.get_obituary_list():
            date_str = obituary.date_str_file
            if date_str not in idx:
                idx[date_str] = []
            idx[date_str].append(obituary)
        return idx

    @classmethod
    def get_first_delta_days(cls):
        obituary_list = cls.get_obituary_list()
        first_ut = obituary_list[-1].ut
        return int((Time.now().ut - first_ut) / SECONDS_IN.DAY)

    @classmethod
    def crawl_uncrawled(cls, n: int):
        delta_days = cls.get_first_delta_days() + 1
        cls.crawl_range(delta_days, delta_days + n - 1)
