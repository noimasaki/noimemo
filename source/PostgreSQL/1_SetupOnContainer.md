# コンテナで PostgreSQL を起動する

## 1. docker-compose による起動

任意のディレクトリで`docker-compose.yml`を作成する。

````bash
├── docker
│   └── postgres
│       ├── docker-compose.yml  # コンテナ起動用
│       └── init.sql            # DB作成用スクリプト
```

```docker
version: '3.9'

services:
  db:
    image: docker.io/library/postgres:latest
    container_name: springtodo-postgres
    restart: always
    shm_size: 128mb
    ports:
      - 5432:5432
    volumes:
      - db-store:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    environment:
      POSTGRES_USER: 'user'                # データベースユーザー
      POSTGRES_PASSWORD: 'postgres'        # データベースパスワード

volumes:
  db-store:
````

docker デーモンを起動してから、`docker-compose.yml`のあるディレクトリで下記を実行してコンテナを起動する。

```
docker compose up -d
```

## 4. DB 作成

`postgres-db-compose.yml`を gitlab-runner ユーザにて、podman-compose up する

```bash
# ユーザスイッチ
sudo -u gitlab-runner -i

# PostgreSQLコンテナ起動
podman-compose -f postgres-db-compose.yml up -d

# コンテナ起動確認
podman ps -a

# コンテナログイン
podman exec -it springtodo-postgres bash

# コンテナ内でPostgreSQLにログイン
psql -U user
```

PostgreSQL にログインできたら、データベース作成する

- データベース設計

| 項目             | 設定          | 備考                                                                                     |
| ---------------- | ------------- | ---------------------------------------------------------------------------------------- |
| DB 名            | springtodo_db |                                                                                          |
| 所有ユーザ       | user          | コンテナ作成時に作成したユーザ                                                           |
| エンコーディング | UTF-8         |                                                                                          |
| 表領域           | pg_default    | 表領域（データベース内のオブジェクトの物理的な保存場所）はデフォルトのディレクトリを利用 |
| 接続数制限       | -1 (無制限)   |                                                                                          |

```bash
# データベース作成
CREATE DATABASE springtodo_db
    WITH OWNER = "user"
         ENCODING = 'UTF8'
         TABLESPACE = pg_default
         CONNECTION LIMIT = -1;

# データベースの一覧を表示 →'q'で終了
\l

# psqlの終了
\q

# 【Ctrl+D】でコンテナから抜ける
```

データベースへの接続情報を`application.properties`および`application-debug.properties`に記載する。

```bash
# DB接続情報
spring.jpa.database=POSTGRESQL
spring.datasource.url=jdbc:postgresql://localhost:5432/springtodo_db
spring.datasource.username=user
spring.datasource.password=postgres
```

ここまでで、SpringBoot を実行してエラーが出なければ DB への接続はできていることが確認できる。（DB 操作はこれから実装していく）

## 5. テーブル作成

SpringBoot 起動時に、クラスパス直下の`schema.sql`を実行するように、`application.properties`に以下を記載

```
spring.sql.init.mode=always
```

`src/main/resources/schema.sql`の内容は

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

-- テストデータ投入 -> 不要になったら削除
INSERT INTO tasks (title, description, status, created_at, updated_at)
VALUES
('Task 1', 'First task description', 'pendingg', '2024-09-01', '2024-09-01'),
('Task 2', 'Second task description', 'in progress', '2024-09-02', '2024-09-03');
```

SpringBoot を起動して、`schema.sql`が想定通りに動いているか確認

```bash
# コンテナログイン
podman exec -it springtodo-postgres bash

# コンテナ内でPostgreSQLにログイン
psql -U user

# springtodo_db データベースに接続
\c springtodo_db

# テーブル一覧を表示
\dt

# 全てのカラムを表示
select * from tasks;
```
