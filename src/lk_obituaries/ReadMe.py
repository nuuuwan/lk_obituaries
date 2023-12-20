import os

from utils import File, Log

from lk_obituaries.SOURCE_LIST import SOURCE_LIST

log = Log('ReadMe')


class ReadMe:
    FILE_PATH = 'README.md'

    @property
    def intro_lines(self) -> list[str]:
        return [
            '# Obituaries (Sri Lanka)',
            '',
            'Crawls data about Obituaries in Sri Lanka.',
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

    @staticmethod
    def get_data_lines_for_source(cls) -> list[str]:
        data_list = cls.get_obituary_list()
        n = len(data_list)
        inner_lines = [
            f'### {cls.get_name()} ({n:,})',
        ]

        prev_month_str = None
        for (
            date_str_file,
            data_list2,
        ) in cls.get_obituary_list_by_date().items():
            month_str = date_str_file[0:7]
            if month_str != prev_month_str:
                inner_lines.append('')
            prev_month_str = month_str

            url = os.path.join(
                cls.get_dir_data(), f'{date_str_file}.json'
            ).replace('\\', '/')
            inner_lines.append(
                f'* [{date_str_file}]({url}) ({len(data_list2):,})'
            )
        return inner_lines

    @property
    def data_lines(self) -> list[str]:
        inner_lines = []
        for cls in SOURCE_LIST:
            inner_lines.extend(self.get_data_lines_for_source(cls))

        return (
            [
                '## Obituaries',
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
