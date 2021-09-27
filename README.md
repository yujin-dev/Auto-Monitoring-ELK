# DB session monitoring

## docker로 ELK 설치
```console
$ docker-compose up -d --build 
```

### ES로 현재 session 기본 정보 전송
`record.py`를 실행

### Kibana 연동
`http://localhost:5601/app/dev_tools#/console` 에서 쿼리 실행하여 결과 추출