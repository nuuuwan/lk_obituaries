from lk_obituaries import SOURCE_LIST, ReadMe

N_UNCRAWLED = 1


def main():
    for cls in SOURCE_LIST:
        cls.crawl_today()
        cls.crawl_uncrawled(N_UNCRAWLED)
    ReadMe().write()


if __name__ == '__main__':
    main()
