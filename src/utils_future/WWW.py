from functools import cached_property

import requests
from bs4 import BeautifulSoup
from utils import Log

log = Log('WWW')


class WWW:
    TIMEOUT = 120
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        + ' AppleWebKit/537.36 (KHTML, like Gecko)'
        + ' Chrome/58.0.3029.110 Safari/537.3'
    }

    def __init__(self, url: str):
        self.url = url

    @cached_property
    def html(self) -> str:
        log.debug(f'Crawling {self.url}')
        return requests.get(
            self.url, headers=WWW.HEADERS, timeout=WWW.TIMEOUT
        ).content

    @property
    def soup(self):
        return BeautifulSoup(self.html, 'html.parser')
