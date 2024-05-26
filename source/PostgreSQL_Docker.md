# PostgreSQLチートシート
- 参考：https://zenn.dev/ayano_sakai/articles/42e64d873bf7df
- 参考：https://hub.docker.com/_/postgres

## PostgreSQL起動
プロジェクトディレクトリ配下に`docker-compose.yml`を作成
```
version: '3.9'

services:
  db:
    image: postgres
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

dockerデーモンを起動してから、コンテナを起動する。
```
docker compose up -d
```




## MySQL チートシート
### 1. コンテナログイン
```
# コンテナID確認
docker ps -a

# コンテナログイン
docker exec -it 【コンテナID】 bash

# コンテナ内でPostgreSQLにログイン
psql -U user
```

### 2. ユーザ作成
```
# ユーザ作成
CREATE USER mrs WITH PASSWORD 'mrs';

# ロール変更
ALTER ROLE mrs NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;
```

### 3. データベース作成
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

# データベースの一覧を表示
\l  #'q'で終了
```

データベースの作成が完了したらPostgreSQLとコンテナから抜ける。
```
user=# CREATE DATABASE mrs
    【省略】
CREATE DATABASE
user=# \q
root@e854c42a0f6c:/# 【Ctrl+D】
exit
```


### 2. テーブル作成

構文は以下の通り
```
CREATE TABLE テーブル名 (
    カラム名1 データ型 [その他のオプション],
    カラム名2 データ型 [その他のオプション],
    ...
);
```

ユーザテーブルの作成例

```
# テーブル作成
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

# データ追加（idはAUTO_INCREMENTなので省略可能）
INSERT INTO user (first_name, last_name, email) VALUES ('Taro', 'Yamada', 'taro.yamada@example.com');
INSERT INTO user (first_name, last_name, email) VALUES ('Hanako', 'Tanaka', 'hanako.tanaka@example.com');
INSERT INTO user (first_name, last_name, email) VALUES ('Jiro', 'Suzuki', 'jiro.suzuki@example.com');

# データ表示
SELECT * FROM user;

# レコード値変更
UPDATE user
SET first_name='masaki', last_name='noi'
WHERE first_name = 'Taro';

# 特定データ削除
DELETE FROM user WHERE first_name = 'Taro';

# 全データ削除
DELETE FROM user;

```

