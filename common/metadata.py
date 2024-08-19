from dataclasses import dataclass

_PREFIX = './data/'
_POSTFIX = '.csv'


def _to_file_name(name: str) -> str:
    return _PREFIX + name + _POSTFIX


def _to_file_name_with_folder(folder: str, file: str) -> str:
    return _PREFIX + folder + file + _POSTFIX


@dataclass
class _CSVName:
    traveler: str
    visit_area_info: str
    codea: str | None = None
    codeb: str | None = None
    sgg: str | None = None
    poi: str | None = None
    travel: str | None = None


@dataclass
class _CSVFolder:
    a: _CSVName
    b: _CSVName
    c: _CSVName
    d: _CSVName


CSV_NAME = _CSVName(
    codea=_to_file_name('codea'),
    codeb=_to_file_name('codeb'),
    sgg=_to_file_name('sgg'),
    poi=_to_file_name('poi'),
    travel=_to_file_name('travel'),
    traveler=_to_file_name('traveler'),
    visit_area_info=_to_file_name('visit_area_info')
)


def get_csv_name(folder: str) -> _CSVName:
    _folder = folder + '/'
    return _CSVName(
        traveler=_to_file_name_with_folder(_folder, 'traveler'),
        visit_area_info=_to_file_name_with_folder(_folder, 'visit_area_info'),
    )


CSV_NAME_V2 = _CSVFolder(
    a=get_csv_name('a'),
    b=get_csv_name('b'),
    c=get_csv_name('c'),
    d=get_csv_name('d'),
)

__all__ = [CSV_NAME, CSV_NAME_V2]
