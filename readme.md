# 패키지 설치

```bash
pip3 install -r requirements.txt
```

# 실행
바로 실행해볼 수 있도록 local 에는 db 와 처음 세팅되었던 secret key 를 넣었습니다.

db 와 secret key 를 따로 지정하려면 settings 아래 local 과 같은 형식으로 파일을 만들어서 그것을 settings 으로 지정하면 됩니다.
```bash
python3 manage.py runserver --settings my_heath.settings.local
```