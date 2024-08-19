# CSV 컬럼 타입 조회
# 특정 컬럼에 타입이 혼합되어 있는 경우가 있음

from common.logger import get_logger
from common.metadata import CSV_NAME_V2
from database.save import DataSaver
from database.model import Place

logger = get_logger('CHECK')

place_savers = [
    DataSaver(CSV_NAME_V2.a.visit_area_info, Place),
    DataSaver(CSV_NAME_V2.b.visit_area_info, Place),
    DataSaver(CSV_NAME_V2.c.visit_area_info, Place),
    DataSaver(CSV_NAME_V2.d.visit_area_info, Place)
]


def check_type(column, saver: DataSaver):
    logger.info(saver)
    saver.load_csv()
    logger.info(saver.data.iloc[:, column].apply(type).unique())


def check_visit_area_type(column: int):
    for saver in place_savers:
        check_type(column, saver)
