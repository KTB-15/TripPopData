# 개발환경 설정
- **Window**
```
.\venv\Scripts\activate
pip install -r requirements.txt
```
- **Mac**
```
source venv/bin/activate
pip3 install -r requirements.txt
```

❗️Interpreter 환경을 `venv/bin/python`으로 맞춰주세요.

# 로컬 DB 연결
Postgresql에서 다음과 같이 설정합니다.
```
- Database name: trippop
- Host: localhost
- Port: 5432
- User: user
- Password: 123456
```