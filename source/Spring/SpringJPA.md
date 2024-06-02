# Spring JPA
SpringでDBへ接続してCRUDする。

## 1. プロジェクト作成
`Spring Initializr`でプロジェクトを作成する。

- Name・Group・Artifact：mrs
- dependencies：Spring Data JPA、PostgreSQL Driver、Thymeleaf、Spring Web

プロジェクトが作成できたらディレクトリ構成を変更する。

```
mrs         # プロジェクトフォルダ
├── HELP.md
├── mvnw
├── mvnw.cmd
├── pom.xml
└── src
    ├── main
    │   ├── java/mrs/mrs
    │   │   ├── MrsApplication.java
    │   │   ├── app             # 追加
    │   │   └── domain          # 追加
    │   │       ├── model       # 追加
    │   │       ├── repository  # 追加
    │   │       └── service     # 追加
    │   └── resources
    │       ├── application.properties
    │       ├── static
    │       └── templates       # HTMLはここ
    └── test/java/mrs/mrs
            └── MrsApplicationTests.java
```

## 2. データベース作成
Dockerで[PostgreSQLコンテナ](https://hub.docker.com/_/postgres)を立てる。

### 2-1. PostgreSQLコンテナ起動
プロジェクトディレクトリ配下に`docker-compose.yml`を作成
```
version: '3.9'

services:
  db:
    image: postgres
    container_name: my_postgres_container
    restart: always
    # set shared memory limit when using docker-compose
    shm_size: 128mb
    ports:
      - 5432:5432
    volumes:
      - db-store:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: 'user'
      POSTGRES_PASSWORD: 'postgres'

volumes:
  db-store:
```

dockerデーモンを起動してから、コンテナを起動し、psqlコマンドでPostgreSQLにログインする。
```
# PostgreSQLコンテナ起動
docker compose up -d

# コンテナ起動確認
docker ps -a

# コンテナログイン
docker exec -it my_postgres_container bash

# コンテナ内でPostgreSQLにログイン
psql -U user
```

### 2-2. ユーザ作成
```
# ユーザ作成
CREATE USER mrs WITH PASSWORD 'mrs';

# ロール変更
ALTER ROLE mrs NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;
```

### 2-3. データベース作成
要件は
- データベース名：mrs
- 所有ユーザ：mrs
- UTF-8エンコーディング
- デフォルトの表領域
- 基本ロケール：C
- 無制限の接続数
PostgreSQLは新しいデータベースを作成するとき、基本的に既存のテンプレートデータベースをコピーして作成する。`TEMPLATE`オプションではそのテンプレートを指定するが、デフォルトの`template1`では今回のロケール`C`とは異なる（`en_US.utf8`がデフォルト）なので、ロケールのカスタマイズが可能な`template0`を指定する。

```
# データベース作成
CREATE DATABASE mrs
    WITH OWNER = mrs
         ENCODING = 'UTF8'
         TABLESPACE = pg_default
         LC_COLLATE = 'C'
         LC_CTYPE = 'C'
         CONNECTION LIMIT = -1
         TEMPLATE = template0;

# データベースの一覧を表示 →'q'で終了
\l

# psqlの終了
\q

# 【Ctrl+D】でコンテナから抜ける
```

### 

## DB接続



