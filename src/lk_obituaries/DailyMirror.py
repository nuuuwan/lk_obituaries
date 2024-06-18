from functools import cached_property

from utils import Log, Time, TimeFormat

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
    def get_emoji(cls) -> str:
        return '🪞'

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
            ps = div.find_all('p')
            if len(ps) <= 1:
                continue
            p = ps[1]
            span_gtime = div.find('span', class_='gtime')
            time_str = span_gtime.text.strip()
            if time_str.lower().endswith('ago'):
                h_ago = int(time_str.split(' ')[0])
                ut = Time.now().ut - h_ago * 3600
            else:
                ut = DailyMirror.TIME_FORMAT_GTIME.parse(time_str).ut

            a = div.find('a')
            url = a['href']

            obituary = Obituary(
                newspaper_id=self.__class__.get_id(),
                ut=int(ut),
                url=url,
                raw_title=h3.text,
                raw_body=p.text,
            )
            obituary_list.append(obituary)
        return obituary_list

    @classmethod
    def crawl_uncrawled(cls, n: int):
        log.warning('[crawl_uncrawled] not implemented')
