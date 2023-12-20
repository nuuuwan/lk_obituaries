from functools import cached_property

from utils import Log

from lk_obituaries.NewsPaper import NewsPaper
from lk_obituaries.Obituary import Obituary
from utils_future import WWW

log = Log('DailyMirror')


class DailyMirror(NewsPaper):
    @classmethod
    def get_name(cls) -> str:
        return 'Daily Mirror'

    @classmethod
    def get_url(cls) -> str:
        return 'https://www.dailymirror.lk/obituaries/378/'

    @cached_property
    def obituary_list(self) -> list[Obituary]:
        url = self.__class__.get_url()
        soup = WWW(url).soup
        div_list = soup.find_all('div', class_='lineg')
        obituary_list = []
        for div in div_list:
            p = div.find_all('p')[1]
            obituary = Obituary(
                newspaper_id=self.__class__.get_id(),
                ut=self.time.ut,
                url=url,
                raw_text=p.text,
            )
            obituary_list.append(obituary)
        return obituary_list

    @classmethod
    def crawl_uncrawled(cls, n: int):
        log.warning('[crawl_uncrawled] not implemented')
