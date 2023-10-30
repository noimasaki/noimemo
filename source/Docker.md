# Docker
javaコンテナを作ってHello World

## 基本コマンド


## フォルダ構成
```
├── Dockerfile
├── docker-compose.yml
└── src
    ├── Main.class
    └── Main.java
```

## 手順
1. Main.java作成 & コンパイル
```
public class Main {

    public static void main(String[] args) {
        System.out.println("Hello, World");
    }
}
```
Main.javaのある階層でコンパイル & 実行テスト
```
> javac Main.java
> java Main
Hello, World
```

2. docker-compose.yml作成
シンプルにjavaコンテナだけを記載したもの
```
version: '3.6'
services:
  java:
    build: .
    tty: true
```

3. Dockerfile作成
```
FROM centos:7
COPY ./src/Main.class Main.class
RUN yum install -y java
RUN java Main
```
- FROM: 利用するベースイメージを指定
- COPY: build時にコンテナイメージへコピーするものを指定
- RUN: build時に実行するコマンド

4. ビルド & 起動
docker-compose.ymlを作成しているので
```
docker compose up -d
```

もし、docker-compose.ymlを作成していないのであれば、ビルドして起動
```
docker build .
docker run -d 【buildしたコンテナイメージ名】
```

コンテナ内に入るには
```
docker exec -it 【docker psからコンテナ名を探す】 bash
```


