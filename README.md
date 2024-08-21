# 개발환경 설정
PostgreSQL이 필요하며,
파이썬 가상환경을 만들어서 작업했습니다.
- **Window**
```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
- **Mac**
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
`virtualenv`가 기본 `venv`를 개선한 패키지라고하니, 이걸 사용해서 만들어도 좋아보입니다.

## CSV 파일 준비
0. 공공데이터에서 csv 데이터를 다운로드합니다.(수도권, 동부권, 서부권, 제주권)
- `Training/라벨링데이터/TL_csv.zip` 폴더를 다운로드 했습니다.
1. `data` 폴더를 생성합니다.
2. 공공데이터 csv 파일의 이름을 다음과 같이 변경합니다.
```
tn_traveller_master_여행객 Master_B -> traveler
tn_visit_area_info_방문지정보_B -> visit_area_info
tc_sgg_시군구코드 -> sgg
```
3. data 폴더 경로에 `sgg.csv`을 넣어줍니다.
4. 하위 폴더로 `a`, `b`, `c`, `d` 폴더를 생성합니다.
- `a`: 수도권, `b`: 동부권, `c`: 서부권, `d`: 제주권
- 공공데이터 상으로 위와 같이 구분되지만, 순서를 지키지 않아도 db 저장에 문제가 없을 것입니다.
5. 각 폴더에 `traveler.csv`와 `visit_area_info.csv`를 넣어줍니다.

❗️Interpreter 환경을 `venv/bin/python`으로 맞춰주세요.

## 로컬 DB 연결
Postgresql에서 다음과 같이 설정합니다.
```
- Database name: trippop
- Host: localhost
- Port: 5432
- User: user
- Password: 123456
```
## 실행하기
```python
insert_all_data(CSV_NAME.sgg, SGG, to_SGG)
insert_all_csv('traveler', Member, to_member)
insert_all_csv('visit_area_info', Place, to_place)
insert_all_csv('visit_area_info', Visit, to_visit)
```
`main.py`에서 위 코드를 순서대로 실행하면
모든 지역의 csv 파일이 가공되어 데이터베이스에 저장됩니다.
`Member`는 `SGG`를 먼저,
`Visit`은 `Place`를 먼저 저장해야 정상적으로 저장될 것입니다.