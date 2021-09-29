# DB session monitoring
`config.py` 에서 기입한 정보를 기반으로 DB 세션을 기록하여 ES 서버에 저장

## docker로 ELK 설치
```console
$ docker-compose up -d --build 
```

### Kibana 연동
`http://localhost:5601/app/dev_tools#/console` 에서 쿼리 실행하여 결과 추출할 수 있다.

### log 확인
- `record.py`를 실행하여 ES로 현재 session 기본 정보 전송한다.
- 주기적으로 session 정보를 저장한다.

#### [ `timestamp`마다의 session count를 확인하는 경우 query ]
```sh
GET session_logger/_search
{
  "size": 0, # hits": [ ] 에 불필요한 도큐먼트 내용이 나타나지 않음
 "aggs": {
   "count_time": {
     "terms": {
       "field": "timestamp"     
     },
     "aggs": {
       "session_count": {
         "value_count": {
           "field": "_id"
         }
       }
     }
   }
 } 
}
```