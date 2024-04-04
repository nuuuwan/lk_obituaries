from functools import cached_property

from utils import TimeUnit, Log, Time, TimeFormat

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

    def __init__(self, delta_days: int):
        self.delta_days = delta_days

    @cached_property
    def time(self) -> Time:
        ut = Time.now().ut - self.delta_days * TimeUnit.SECONDS_IN.DAY
        ut = int(ut / TimeUnit.SECONDS_IN.DAY) * TimeUnit.SECONDS_IN.DAY
        return Time(ut)

    @cached_property
    def obituary_list(self) -> list[Obituary]:
        raise NotImplementedError

    @cached_property
    def date_str_file(self) -> str:
        return NewsPaper.TIME_FORMAT_FILE.stringify(self.time)

    @classmethod
    def get_first_delta_days(cls):
        obituary_list = Obituary.list_for_newspaper(cls.get_id())
        first_ut = obituary_list[-1].ut
        return int((Time.now().ut - first_ut) / TimeUnit.SECONDS_IN.DAY)

    def crawl(self):
        log.debug(
            f'[crawl] {self.__class__.get_id()}-{self.date_str_file}...'
        )

        for obituary in self.obituary_list:
            obituary.write()

    @classmethod
    def crawl_today(cls):
        cls(0).crawl()

    @classmethod
    def crawl_range(cls, min_delta_days: int, max_delta_days: int):
        for delta_days in range(min_delta_days, max_delta_days + 1):
            log.debug(f'[crawl_range] {delta_days}/{max_delta_days}')
            cls(delta_days).crawl()

    @classmethod
    def crawl_uncrawled(cls, n: int):
        delta_days = cls.get_first_delta_days() + 1
        cls.crawl_range(delta_days, delta_days + n - 1)
