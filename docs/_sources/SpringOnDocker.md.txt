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
- dependencies: Spring Web
上記は例なので適宜変更すること

完了するとプロジェクトが作成される
![VS Code](_static/SpringOnDocker/2_init.png)

2. Controllerの作成
Controller.javaを新規作成する
![VS Code](_static/SpringOnDocker/3_controller.png)

Controller.java
```

```