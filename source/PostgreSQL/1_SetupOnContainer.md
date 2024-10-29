# コンテナで PostgreSQL を起動する

docker-compose を利用して、PostgreSQL を起動し、データベースとテーブルを作成する。

## 1. docker-compose.yml の作成

任意のディレクトリで`docker-compose.yml`を作成する。

````bash
├── docker
│   └── postgres
│       ├── docker-compose.yml  # コンテナ起動用
│       ├── init.sql            # DB作成用スクリプト（必要であれば）
│       └── schema.sql          # テーブル作成用スクリプト（必要であれば）
```

```docker
version: '3.9'

services:
  db:
    image: docker.io/library/postgres:latest
    container_name: my-postgres
    restart: always
    shm_size: 128mb
    ports:
      - 5432:5432
    volumes:
      - my-db-store:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql   # DB作成用スクリプト（必要であれば）
    environment:
      POSTGRES_USER: 'user'                # データベースユーザー
      POSTGRES_PASSWORD: 'postgres'        # データベースパスワード

volumes:
  my-db-store:
````

## 2. DB 作成スクリプト

必要であれば、DB 作成用スクリプト作成する。

```sql
CREATE DATABASE my_app_db
    WITH OWNER = "user"
        ENCODING = 'UTF8'
        TABLESPACE = pg_default
        CONNECTION LIMIT = -1;

```

## 3. テーブル作成スクリプト

DB の中のテーブル作成スクリプトを作成する。
SpringBoot においては、application.properties などで指定すれば、DB 接続して自動で実行したりもできるが、ここではスクリプトだけを記載し、実行方法については言及しない。

```sql
DROP TABLE IF EXISTS tasks CASCADE ;

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL NOT NULL,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    status VARCHAR(255),
    created_at DATE NOT NULL,
    updated_at DATE NOT NULL,
    PRIMARY KEY (id)
) ;

-- テストデータ投入
INSERT INTO tasks (title, description, status, created_at, updated_at)
VALUES
('Task 1', 'First task description', 'pendingg', '2024-09-01', '2024-09-01'),
('Task 2', 'Second task description', 'in progress', '2024-09-02', '2024-09-03');
```

## 4. コンテナ起動

docker デーモンを起動してから、`docker-compose.yml`のあるディレクトリで下記を実行してコンテナを起動する。

```
docker compose up -d
```

もしくは、ファイル指定する場合には`-f` オプションを利用する。

```
docker-compose -f ./docker/postgres/docker-compose.yml up -d
```

コンテナ起動から、実際にデータベースが作成されているかなどを確認するコマンドの流れ。

```bash
# ----- コンテナ起動・DB作成確認 ------
# PostgreSQLコンテナ起動
docker-compose -f ./docker/postgres/docker-compose.yml up -d

# コンテナ起動確認
docker ps -a

# コンテナログイン
docker exec -it my-postgres bash

# コンテナ内でPostgreSQLにログイン
psql -U user

# データベースの一覧を表示 -> my_app_dbが作成されていることを確認
\l

# 'q'で終了

# psqlの終了
\q

# 【Ctrl+D】でコンテナから抜ける

# ----- テーブル作成・テーブル確認 ------
# スキーマ実行
docker exec -i my-postgres psql -U user -d my_app_db < ./docker/postgres/schema.sql

# コンテナログイン
docker exec -it my-postgres bash

# コンテナ内でPostgreSQLにログイン
psql -U user

# my_app_db データベースに接続
\c my_app_db

# テーブル一覧を表示 -> スキーマで定義したテーブルが表示されること
\dt

# 全てのカラムを表示 -> 投入したテストデータが表示されること
select * from tasks;

```
