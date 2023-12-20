from utils import TIME_FORMAT_TIME, File, Log, Time

from lk_obituaries.Obituary import Obituary
from lk_obituaries.SOURCE_LIST import SOURCE_LIST

log = Log('ReadMe')


class ReadMe:
    FILE_PATH = 'README.md'

    @property
    def intro_lines(self) -> list[str]:
        time_str = TIME_FORMAT_TIME.stringify(Time.now())

        return [
            '# Obituaries (Sri Lanka)',
            '',
            'Crawls data about Obituaries in Sri Lanka.',
            '',
            f'Last run at **{time_str}**.',
            '',
        ]

    @property
    def source_lines(self) -> list[str]:
        inner_lines = []
        for cls in SOURCE_LIST:
            inner_lines.append(f'* [{cls.get_name()}]({cls.get_url()})')

        return (
            [
                '## Sources',
                '',
            ]
            + inner_lines
            + ['']
        )

    @property
    def data_lines(self) -> list[str]:
        inner_lines = []
        obituary_list = Obituary.list_all()
        n = len(obituary_list)

        prev_month_str = None
        for obituary in obituary_list:
            date_str = obituary.date_str
            month_str = date_str[:7]
            if month_str != prev_month_str:
                inner_lines.extend([f'### {month_str}', ''])
                prev_month_str = month_str

            inner_lines.append(
                f'* [{obituary.file_only}]({obituary.data_path})'
            )

        return (
            [
                f'## List of Obituaries ({n:,})',
                '',
            ]
            + inner_lines
            + ['']
        )

    @property
    def lines(self) -> list[str]:
        return self.intro_lines + self.source_lines + self.data_lines

    def write(self):
        File(self.FILE_PATH).write_lines(self.lines)
        log.info(f'Wrote {self.FILE_PATH}')
