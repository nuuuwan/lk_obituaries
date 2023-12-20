from functools import cached_property

from utils import Log, TimeFormat

from lk_obituaries.NewsPaper import NewsPaper
from lk_obituaries.Obituary import Obituary
from utils_future import WWW

log = Log('DailyMirror')


class DailyMirror(NewsPaper):
    TIME_FORMAT_GTIME = TimeFormat('%d %b %Y')

    @classmethod
    def get_name(cls) -> str:
        return 'Daily Mirror'

    @classmethod
    def get_url(cls) -> str:
        return 'https://www.dailymirror.lk/obituaries/378/'

    @cached_property
    def obituary_list(self) -> list[Obituary]:
        soup = WWW(self.__class__.get_url()).soup
        div_list = soup.find_all('div', class_='lineg')
        obituary_list = []
        for div in div_list:
            h3 = div.find('h3')
            p = div.find_all('p')[1]
            span_gtime = div.find('span', class_='gtime')
            print("'%s'" % span_gtime.text)
            ut = DailyMirror.TIME_FORMAT_GTIME.parse(
                span_gtime.text.strip()
            ).ut
            a = div.find('a')
            url = a['href']

            obituary = Obituary(
                newspaper_id=self.__class__.get_id(),
                ut=ut,
                url=url,
                raw_title=h3.text,
                raw_body=p.text,
            )
            obituary_list.append(obituary)
        return obituary_list

    @classmethod
    def crawl_uncrawled(cls, n: int):
        log.warning('[crawl_uncrawled] not implemented')
