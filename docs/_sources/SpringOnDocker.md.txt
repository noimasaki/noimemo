# Spring BootをDocker上で動かす

Spring Bootで作成したHello WorldをJarファイルにビルドして、Docker上で動かす。

↓ディレクトリ構成
```

```

## Spring Bootアプリの作成
1. Spring InitializrからMavenプロジェクトを作成
![VS Code](_static/SpringOnDocker/1_init.png)

- Spring Boot version: 3.15
- project language: Java
- Group Id: com.example
- Artifact Id: hello
- packaging type: Jar
- Java version: 17  ※Dockerイメージ作成するときに合わせる必要があるので注意
- dependencies: Tymeleaf、Spring Web、Lombok、Spring Boot DevTools

上記は例なので適宜変更すること

【補足：dependenciesについて】


完了するとプロジェクトが作成される
![VS Code](_static/SpringOnDocker/2_init.png)

2. Controller、htmlの作成
HelloController.javaを新規作成する
![VS Code](_static/SpringOnDocker/3_controller.png)

HelloController.java
```
package com.example.hello;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HelloController {
    @GetMapping("/hello")       # localhost:8080/hello でアクセス来たらhelloworld()を実行
    public String helloworld() {
        return("Hello");        # ~src/main/resources/templates/Hello.html をreturn
    }
}
```

Hello.htmlを新規作成する
![VS Code](_static/SpringOnDocker/4_html.png)

```
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Sample</title>
</head>
<body>
    <h1>Hello World!</h1>
</body>
</html>
```

3. 動作確認
HelloApprication.javaを実行
![VS Code](_static/SpringOnDocker/5_test.png)

ブラウザからアクセスして確認
![test](_static/SpringOnDocker/6_test.png)

4. Mavenでビルド
SpringBootのソースディレクトリ（pom.xmlがあるところ）でビルドコマンド実行
```
mvn package spring-boot:repackage
```

targetフォルダはいかに`.jar`ファイルが生成される
![jar](_static/SpringOnDocker/7_jar.png)


## コンテナイメージ作成
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


## 参考
### Apache Maven インストール（Windows）
1. [Apache Maven サイト](https://maven.apache.org/)から、`Binary zip archive`をダウンロード&展開して、C:\直下に配置
![MavenInstall](_static/SpringOnDocker/99_MavenInstall.png)

2. システム環境変数Pathに`C:\apache-maven-3.9.5\bin`を追加

3. `mvn -v`コマンドを実行してインストールされていることを確認