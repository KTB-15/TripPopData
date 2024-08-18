from database.conn import Base
from common.logger import get_logger
from database.model import Member, SGG

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


def to_SGG(data) -> Base:
    # 필드값 없는 데이터는 불량으로 간주
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


def to_member(data) -> Base:
    # 필드값 없는 데이터는 불량으로 간주
    for field in MEMBER_CSV_FIELD:
        if pd.isna(data[field]):
            _logger.info(f"SKIP member {data}")
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
    _logger.info(f"Member(id: {member.id}, gender: {member.gender}, sgg: {member.travel_like_sgg}, sido: {member.travel_like_sido})")
    return member
