from database.conn import Base, get_filter
from common.logger import get_logger
from database.model import Member, SGG, Place, Visit
from typing import Union

import pandas as pd
import datetime

_logger = get_logger('FORMAT')

'''
최신 작업일자: 24/08/19
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
            # _logger.warning(f"SKIP place {data['TRAVEL_ID']}, visit type: {data['VISIT_AREA_TYPE_CD']}")
            return None

    # x 좌표, y 좌표가 숫자인지 확인
    x_coord, y_coord = float(), float()
    try:
        x_coord = float(data['X_COORD'])
        y_coord = float(data['Y_COORD'])
    except ValueError:
        _logger.warning(f"이상한 좌표: {(data['X_COORD'], data['Y_COORD'])}")

    place = Place(
        area_name=data['VISIT_AREA_NM'],
        road_name=data['LOTNO_ADDR'],
        x_coord=x_coord,
        y_coord=y_coord
    )
    # _logger.info(place)
    return place


'''
///
CSV FIELD - DB FIELD (필터링 조건)
///
없음 - id(시퀀스 넘버 만들어야함 AUTO)
TRAVEL_ID - member_id(prefix 제거 필요. 2번째 인덱스부터 저장)
DB 조회 - place_id(방문지명(area_name)을 조회해서 얻어야함)
RESIDENCE_TIME_MIN - residence_time
VISIT_AREA_TYPE_CD - visit_type_code (1 ~ 8 유형만)
REVISIT_YN - revisit_yn(Y -> True, N -> False로 매핑)
DGSTFN - rating (1 ~ 5)
REVISIT_INTENTION - revisit_intention (1 ~ 5)
'''

VISIT_CSV_FIELD = [
    'TRAVEL_ID', 'VISIT_AREA_TYPE_CD'
]


def to_visit(data: pd.DataFrame) -> Union[Base, None]:
    # 필드값 없는 데이터는 불량으로 간주
    for field in VISIT_CSV_FIELD:
        if pd.isna(data[field]):
            # _logger.warning(f"SKIP visit {data}")
            return None
    # 해당 방문지 있는지 확인, 없으면 무시
    place = get_filter('area_name', Place, data['VISIT_AREA_NM'])
    if not place:
        # _logger.warning(f"SKIP visit {data['TRAVEL_ID'][2:]}: NOT FOUND PLACE")
        return None
    # _logger.info(f"PLACE OF VISIT: {place.id}, MEMBER OF VISIT: {data['TRAVEL_ID'][2:]}")
    visit = Visit(
        member_id=data['TRAVEL_ID'][2:],
        place_id=place.id,
        residence_time=int(data['RESIDENCE_TIME_MIN']),
        visit_type_code=int(data['VISIT_AREA_TYPE_CD']),
        revisit_yn=True if data['REVISIT_YN'] else False,
        rating=int(data['DGSTFN']),
        revisit_intention=int(data['REVISIT_INTENTION'])
    )
    # _logger.info(visit)
    return visit


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
