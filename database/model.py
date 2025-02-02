from sqlalchemy import Boolean, Column, Integer, Double, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.conn import Base


class Member(Base):
    __tablename__ = 'member'

    id = Column(String, primary_key=True, unique=True, nullable=False)
    member_id = Column(String)  # 아이디
    password = Column(String)
    nickname = Column(String)
    gender = Column(String)  # Male / Female
    age = Column(Integer)
    travel_style_1 = Column(String)  # 여행스타일1(자연 vs 도시)
    travel_style_2 = Column(String)  # 여행스타일2(숙박 vs 당일)
    travel_style_3 = Column(String)  # 여행스타일3(새로운지역 vs 익숙한지역)
    travel_style_4 = Column(String)  # 여행스타일4(비싼 숙소 vs 불편한 숙소)
    travel_style_5 = Column(String)  # 여행스타일5(휴양 vs 체험활동)
    travel_style_6 = Column(String)  # 여행스타일6(알려지지 않은 방문지 vs 핫플)
    travel_style_7 = Column(String)  # 여행스타일7(계획적 vs 즉흥적)
    travel_style_8 = Column(String)  # 여행스타일8(사진 중요 vs 안중요)
    register_at = Column(String)
    activated = Column(Boolean)

    visits = relationship('Visit', back_populates='member')
    favourites = relationship('Favourite', back_populates='member')
    reviews = relationship('Review', back_populates='member')
    histories = relationship('History', back_populates='member')

    def __str__(self):
        return f"Member(id: {self.id}, gender: {self.gender}, sgg: {self.travel_like_sgg})"


class Visit(Base):
    __tablename__ = 'visit'

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    member_id = Column(String, ForeignKey('member.id'), nullable=False)
    place_id = Column(Integer, ForeignKey('place.id'), nullable=False)
    residence_time = Column(Integer)  # 체류시간 (분 단위)
    visit_type_code = Column(Integer)  # 방문지 유형 코드
    revisit_yn = Column(Boolean)  # 재방문 여부(Y, N)
    rating = Column(Integer)  # 만족도 (1 ~ 5)
    revisit_intention = Column(Integer)  # 재방문 의향 (1 ~ 5)

    member = relationship('Member', back_populates='visits')
    place = relationship('Place', back_populates='visits')

    def __str__(self):
        return f"Visit(member: {self.member_id}, place: {self.place_id}, visit_code: {self.visit_type_code}, rating: {self.rating})"


class Place(Base):
    __tablename__ = 'place'

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    area_name = Column(String, unique=True)  # 방문지 이름
    road_name = Column(String)  # 도로명 주소
    x_coord = Column(Double)  # 경도
    y_coord = Column(Double)  # 위도
    image_url = Column(String)

    visits = relationship('Visit', back_populates='place')
    favourites = relationship('Favourite', back_populates='place')
    reviews = relationship('Review', back_populates='place')
    histories = relationship('History', back_populates='place')

    def __str__(self):
        return f"Place(area name: {self.area_name}, coord: {(self.x_coord, self.y_coord)}"


class SGG(Base):
    __tablename__ = 'sgg'

    id = Column(String, primary_key=True, unique=True, nullable=False)  # 시도 코드(2자리) + 시군구 코드(3자리)
    sido_code = Column(Integer)
    sgg_code = Column(Integer)
    sido_name = Column(String)  # 시도 이름
    sgg_name = Column(String)  # 시군구 이름


    def __str__(self):
        return f"SGG(id={self.id}, sido_name={self.sido_name}, sgg_name={self.sgg_name})"


class Favourite(Base):
    __tablename__ = 'favourite'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    member_id = Column(String, ForeignKey('member.id'), nullable=False)
    place_id = Column(String, ForeignKey('place.id'), nullable=False)
    register_at = Column(Date)

    member = relationship('Member', back_populates='favourites')
    place = relationship('Place', back_populates='favourites')


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    member_id = Column(String, ForeignKey('member.id'), nullable=False)
    place_id = Column(String, ForeignKey('place.id'), nullable=False)
    content = Column(Text)
    register_at = Column(Date)
    updated_at = Column(Date)

    member = relationship('Member', back_populates='reviews')
    place = relationship('Place', back_populates='reviews')


class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    member_id = Column(String, ForeignKey('member.id'), nullable=False)
    place_id = Column(String, ForeignKey('place.id'), nullable=False)
    content = Column(Text)
    register_at = Column(Date)
    updated_at = Column(Date)

    member = relationship('Member', back_populates='histories')
    place = relationship('Place', back_populates='histories')
