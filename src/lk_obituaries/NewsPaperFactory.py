from lk_obituaries.DailyMirror import DailyMirror
from lk_obituaries.DailyNews import DailyNews


class NewsPaperFactory:
    @staticmethod
    def list_all():
        return [
            DailyMirror,
            DailyNews,
        ]

    @staticmethod
    def idx():
        return {cls.get_id(): cls for cls in NewsPaperFactory.list_all()}

    @staticmethod
    def from_id(id: str):
        return NewsPaperFactory.idx()[id]
