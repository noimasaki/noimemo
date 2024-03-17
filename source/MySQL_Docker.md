# MySQLチートシート
- 参考：https://zenn.dev/ryo7/articles/create-mysql-on-docker
- 参考：https://qiita.com/taniann/items/ed9ec892d91e5af962c6



## MySQL起動
### (a) Docker Compose不使用
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

### (b) Docker Compose利用
** ToDo: 執筆予定 **


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

# データ追加（詳細は後述）
INSERT INTO db_name.tbl_name (col_name1, col_name2, ...)
  VALUES (value1, value2, ...);

```

### 2. テーブル操作