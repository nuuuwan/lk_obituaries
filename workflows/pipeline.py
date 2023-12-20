import os

from utils import Log

from lk_obituaries import NewsPaperFactory, ReadMe

log = Log('pipeline')


TEST_MODE = os.name == 'nt'
log.debug(f'{TEST_MODE=}')

N_UNCRAWLED = 1 if TEST_MODE else 28
log.debug(f'{N_UNCRAWLED=}')


def main():
    for cls in NewsPaperFactory.list_all():
        cls.crawl_today()
        cls.crawl_uncrawled(N_UNCRAWLED)

    ReadMe().write()


if __name__ == '__main__':
    main()
