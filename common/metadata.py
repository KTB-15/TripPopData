from dataclasses import dataclass

_PREFIX = './data/'
_POSTFIX = '.csv'


def _to_file_name(name: str) -> str:
    return _PREFIX + name + _POSTFIX


@dataclass
class _CSVName:
    codea: str
    codeb: str
    sgg: str
    poi: str
    travel: str
    traveler: str
    visit_area_info: str


CSV_NAME = _CSVName(
    codea=_to_file_name('codea'),
    codeb=_to_file_name('codeb'),
    sgg=_to_file_name('sgg'),
    poi=_to_file_name('poi'),
    travel=_to_file_name('travel'),
    traveler=_to_file_name('traveler'),
    visit_area_info=_to_file_name('visit_area_info')
)

__all__ = [CSV_NAME]
