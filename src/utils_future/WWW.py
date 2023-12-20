from functools import cached_property

import requests
from bs4 import BeautifulSoup
from utils import Log

log = Log('WWW')


class WWW:
    TIMEOUT = 60

    def __init__(self, url: str):
        self.url = url

    @cached_property
    def html(self) -> str:
        log.debug(f'Crawling {self.url}')
        return requests.get(self.url, timeout=WWW.TIMEOUT).content

    @property
    def soup(self):
        return BeautifulSoup(self.html, 'html.parser')
