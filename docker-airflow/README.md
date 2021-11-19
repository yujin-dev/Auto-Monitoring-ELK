## docker-airflow

*(출처) https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html*

postgresql을 DB로 연결하여 docker-compose로 airflow를 실행한다.

**[ 컨테이너 실행 ]**
- airflow-webserver
- airflow-scheduler
- postgres

1. airflow-init
AIRFLOW_UID와 airflow User를 세팅한다. 아래와 같이 실행하여 데이터베이스를 초기화한다.

```console
$ echo -e "AIRFLOW_UID=$(id -u)" > .env
$ docker-compose up airflow-init
--------------------------------
...
airflow-init_1       | [2021-11-18 08:54:24,346] {manager.py:214} INFO - Added user airflow
airflow-init_1       | User "airflow" created with role "Admin"
airflow-init_1       | 2.2.2
```

2. 재시작하려면 volumes, 연동되지 않은 컨테이너를 정리한다.
```console
$ docker-compose down --volumes --remove-orphans
```

3. services를 실행한다.
```console
$ docker-compose up
```

4. airflow에 접속한다.
services가 실행 중이라면 CLI 명령어로 접근할 수 있다.
```console
$ curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.2.2/airflow.sh'
$ chmod +x airflow.sh

$ ./airflow.sh bash
$ ./airflow.sh python
```

UI는 `{host}:8080`에 접속하여 `_AIRFLOW_WWW_USER_USERNAME`, `_AIRFLOW_WWW_USER_PASSWORD`으로 들어갈 수 있다. 



*(참고)*
- 이미지 직접 빌드하기 : https://airflow.apache.org/docs/docker-stack/build.html