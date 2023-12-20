from functools import cached_property

from utils import Log, TimeFormat

from lk_obituaries.NewsPaper import NewsPaper
from lk_obituaries.Obituary import Obituary
from utils_future import WWW

log = Log('DailyNews')


class DailyNews(NewsPaper):
    @classmethod
    def get_name(cls) -> str:
        return 'Daily News'

    @classmethod
    def get_url(cls) -> str:
        return 'https://www.dailynews.lk'

    @cached_property
    def date_str(self) -> str:
        return TimeFormat('%Y/%m/%d').stringify(self.time)

    @cached_property
    def url(self) -> str:
        return f"{self.__class__.get_url()}/{self.date_str}/obituaries/"

    @cached_property
    def url2(self):
        w = WWW(self.url)
        soup = w.soup
        h2 = soup.find('h2', class_='penci-entry-title')
        if h2 is None:
            log.debug('[url2] h2 is None')
            log.debug(w.html)
            return None
        obituary_link = h2.find('a', string='Obituaries')
        if obituary_link is None:
            log.debug('[url2] obituary_link is None')
            return None
        return obituary_link['href']

    @cached_property
    def obituary_list(self) -> list[Obituary]:
        if self.url2 is None:
            return []
        soup = WWW(self.url2).soup
        div = soup.find('div', id='penci-post-entry-inner')
        obituary_list = []
        for i, p in enumerate(div.find_all('p')):
            obituary = Obituary(
                newspaper_id=self.__class__.get_id(),
                ut=self.time.ut,
                date_str_file=self.date_str_file,
                i=i,
                raw_text=p.text,
            )
            obituary_list.append(obituary)
        return obituary_list
