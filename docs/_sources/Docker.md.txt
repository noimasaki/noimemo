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




## Mavenでビルド
SpringBootのソースディレクトリ（pom.xmlがあるところ）でビルドコマンド実行
```
mvn package spring-boot:repackage
```

targetフォルダ配下にビルドされたjarファイルが生成される

## Dockerビルド
Dockerfileを作成
```
FROM centos:7
COPY ./hello/target/*.jar app.jar
EXPOSE 8080
RUN yum install -y java-17-openjdk
ENTRYPOINT ["java","-jar","app.jar"] #コンテナが起動する際に実行されるコマンド。「java -jar app.jar」が実行される
```

docker-composeを作成
```
version: '3.6'
services:
  java:
    build: .
    tty: true
```

ビルドの実行
```
docker build \
    --no-cache \
    --tag app-hello-spring-boot:latest .
```

コンテナ起動
```
docker run --rm \
    --publish 8080:8080 \
    --name app-local \
    app-hello-spring-boot
```