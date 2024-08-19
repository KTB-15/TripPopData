from database.conn import Base
from common.logger import get_logger
from database.model import Member, SGG, Place
from typing import Union

import pandas as pd
import datetime

_logger = get_logger('FORMAT')

'''
최신 작업일자: 24/08/18
'''

'''
///
CSV FIELD - DB FIELD (필터링 조건)
///
SGG_CD - id(11자리 수이지만 시도(첫 2 자리)와 시군구(그 다음 3 자리)를 합친 것만 id로 한다. member 필드와 연관돼있음.)
SIDO_NM - sido_name
SGG_NM - sgg_name
'''


def to_SGG(data) -> Union[Base, None]:
    # 필드값 없는 데이터는 불량으로 간주
    if pd.isna(data['SGG_CD']) or pd.isna(data['SIDO_NM']) or pd.isna(data['SGG_NM']):
        _logger.info(f"SKIP sgg {data}")
        return None
    sgg_cd = str(data['SGG_CD'])[:5]
    sgg = SGG(
        id=sgg_cd,
        sido_name=data['SIDO_NM'],
        sgg_name=data['SGG_NM']
    )
    _logger.info(sgg)
    return sgg


'''
///
CSV FIELD - DB FIELD (필터링 조건)
///
없음 - id(시퀀스 넘버 만들어야함 AUTO)
VISIT_AREA_NM - area_name(주소명, unique해야함)
LOTNO_ADDR - road_name(원래는 도로명 주소를 넣으려 했는데, 없는 경우가 있어서 지번 주소로 넣으려함)
X_COORD - x_coord
Y_COORD - y_coord
'''

PLACE_CSV_FIELD = [
    'VISIT_AREA_NM', 'LOTNO_ADDR', 'X_COORD', 'Y_COORD', 'VISIT_AREA_TYPE_CD'
]

def is_valid_visit_type(status: int) -> bool:
    return 1 <= status <= 8

def to_place(data) -> Union[Base, None]:
    # 데이터 무시
    for field in PLACE_CSV_FIELD:
        # 필드 값 누락 또는 불필요 방문 유형 필터링
        if pd.isna(data[field]) or not is_valid_visit_type(data['VISIT_AREA_TYPE_CD']):
            _logger.warning(f"SKIP place {data}")
            return None

    place = Place(
        area_name=data['VISIT_AREA_NM'],
        road_name=data['LOTNO_ADDR'],
        x_coord=data['X_COORD'],
        y_coord=data['Y_COORD']
    )
    _logger.info(place)
    return place


'''
///
CSV FIELD - DB FIELD (필터링 조건)
///

'''


def to_visit(data) -> Union[Base, None]:
    return Base()


'''
///
CSV FIELD - DB FIELD (필터링 조건)
///
TRAVELER_ID - id
GENDER - gender(남 -> Male, 여 -> Female)
AGE_GRP - age(10 단위)
TRAVEL_STYL_1 - travel_style_1 (범위: 1 ~ 7)
TRAVEL_LIKE_SIDO_1 - travel_like_sido
TRAVEL_LIKE_SGG_1 - travel_like_sgg
'''

MEMBER_CSV_FIELD = ['TRAVELER_ID', 'GENDER', 'AGE_GRP', 'TRAVEL_STYL_1', 'TRAVEL_STYL_2', 'TRAVEL_STYL_3',
                    'TRAVEL_STYL_4', 'TRAVEL_STYL_5', 'TRAVEL_STYL_6', 'TRAVEL_STYL_7', 'TRAVEL_STYL_8',
                    'TRAVEL_LIKE_SIDO_1', 'TRAVEL_LIKE_SGG_1']


def to_member(data) -> Union[Base, None]:
    # 필드값 없는 데이터는 불량으로 간주
    for field in MEMBER_CSV_FIELD:
        if pd.isna(data[field]):
            _logger.warning(f"SKIP member {data}")
            return None
    member = Member(
        id=data['TRAVELER_ID'],
        gender='MALE' if data['GENDER'] == '남' else 'FEMALE',
        age=data['AGE_GRP'],
        travel_like_sgg=data['TRAVEL_LIKE_SGG_1'],
        travel_like_sido=data['TRAVEL_LIKE_SIDO_1'],
        travel_style_1=data['TRAVEL_STYL_1'],
        travel_style_2=data['TRAVEL_STYL_2'],
        travel_style_3=data['TRAVEL_STYL_3'],
        travel_style_4=data['TRAVEL_STYL_4'],
        travel_style_5=data['TRAVEL_STYL_5'],
        travel_style_6=data['TRAVEL_STYL_6'],
        travel_style_7=data['TRAVEL_STYL_7'],
        travel_style_8=data['TRAVEL_STYL_8'],
        register_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    _logger.info(member)
    return member
