# Docker
javaコンテナを作ってHello World

## フォルダ構成
```
├── docker
│   └── java
│       └── Dockerfile
├── docker-compose.yml
└── server
    └── src
        ├── Main.class
        └── Main.java

```

## 手順
1. docker-compose.yml作成
```
version: '3.6'
services:
  java:
    build: ./docker/java
    ports:
      - 8080:8080
    tty: true
    volumes:
      - ./server/src:/usr/src:cached
```

2. Dockerfile作成

3. Main.java作成 & コンパイル
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