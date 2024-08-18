from database.conn import Base
from common.logger import get_logger
from database.model import SGG

import pandas as pd

_logger = get_logger('FORMAT')


def to_SGG(data) -> Base:
    if pd.isna(data['SGG_CD']) or pd.isna(data['SIDO_NM']) or pd.isna(data['SGG_NM']):
        _logger.info(f"SKIP sgg {data}")
        return None
    sgg_cd = str(data['SGG_CD'])[:5]
    _logger.info(f"{sgg_cd}, {data['SIDO_NM']}, {data['SGG_NM']}")
    sgg = SGG(
        id=sgg_cd,
        sido_name=data['SIDO_NM'],
        sgg_name=data['SGG_NM']
    )
    return sgg


def to_place(data) -> Base:
    return Base()


def to_visit(data) -> Base:
    return Base()


def to_member(data) -> Base:
    return Base()
