# DB session monitoring
`config.py` 에서 기입한 정보를 기반으로 DB 세션을 기록하여 ES 서버에 저장

## docker로 ELK 설치
```console
$ docker-compose up -d --build 
```

### ES로 현재 session 기본 정보 전송
`record.py`를 실행

### Kibana 연동
`http://localhost:5601/app/dev_tools#/console` 에서 쿼리 실행하여 결과 추출