# MySQLチートシート
- 参考：https://zenn.dev/ryo7/articles/create-mysql-on-docker
- 参考：https://qiita.com/taniann/items/ed9ec892d91e5af962c6



## MySQL起動（Docker Compose不使用）
ひとまずお試しする場合。データの永続化を実施しないとDBに書き込んだデータがコンテナ削除に伴って消えてしまうので、後述のDocker Composeを利用すること。

```
# Docker-hubからMySQLのイメージをインストールする
$ docker pull mysql

# インストールしたイメージから、コンテナを起動･作成する
# MYSQL_ROOT_PASSWORDにログインする際のパスワードを設定する
$ docker run -it --name test-wolrd-mysql -e MYSQL_ROOT_PASSWORD=mysql -d mysql:latest

# 起動したMySQLコンテナにログインする
$ docker exec -it test-wolrd-mysql bash -p

# コンテナ上で動作するMySQLにログインする
$ mysql -u root -p -h 127.0.0.1

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 10
Server version: 8.0.16 MySQL Community Server - GPL

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

> mysql
```

## MySQL起動（Docker Compose）
フォルダ構成は以下

```
.
├── docker-compose.yml
└── mysql
    ├── Dockerfile
    ├── db　：永続化のための空領域
    ├── initdb.d
    │   └── init.sql
    └── my.cnf
```

Docerfileの記載（デフォルトのままなので作成する意味はない）
```
#使うDockerイメージ
FROM mysql

#ポートの設定
EXPOSE 3306

#docker run時の実行コマンド
CMD ["mysqld"]
```

docker-compose.yml
```
version: "3"

services:
  mysql:
    image: mysql:latest
    container_name: test-world-mysql
    environment:
      - MYSQL_ROOT_PASSWORD=mysql
    ports:
      - "3306:3306"
    volumes:
      - ./mysql/db:/var/lib/mysql #ここにデータ永続化するためのファイルが入る。

volumes:
  mysql-data:
```



## MySQL チートシート
- 参考：https://qiita.com/hryshtk/items/dd69db351bb47f57b4e1

### 1. データベース作成/削除

```
# MySQLへのログイン
mysql -u root -p

# データベースの一覧を表示
SHOW DATABASES;

# データベース作成
CREATE DATABASE データベース名;

# データベース削除
DROP DATABASE データベース名;

# データベース接続
USE データベース名;

# データベースを指定してテーブル一覧表示
SHOW TABLES FROM データベース名;

# 接続したデータベースのテーブル一覧表示
SHOW TABLES;

# テーブル作成（詳細は後述）
CREATE TABLE データベース名.テーブル名 
(col_name1 data_type1, col_name2 data_type2, ...);

# テーブル削除
DROP TABLE テーブル名;

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

