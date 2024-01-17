# マイクロサービス作成
## 実施すること
認証認可機能を持ったBFF（Backend for Frontend）と、商品情報のCRUD操作のAPIを提供するバックエンドサービスを作成する。

ユーザはブラウザからBFFにアクセスし、認証成功後にバックエンドサービスにアクセスすることができる。

## 作成の流れ
1. BFFの作成
2. バックエンドの作成
3. BFF改修：BFF -> バックエンドへアクセス可能とする
4. BFF改修：バックエンドから受け取ったjsonを画面に表示する

# 1. BFFの作成
1. プロジェクト作成（Spring Initializr）
- Java: 17
- SpringBoot: 3.2.1
- dependencies: spring-boot-starter-web
- dependencies: spring-boot-starter-security
- dependencies: spring-boot-starter-thymeleaf

1. ディレクトリ構成変更
可読性向上の為、`.java`が含まれるディレクトリを以下のように変更する。
```bash
SpringMicroservice/frontend-webapp/src/main
├── java
│   └── com
│       └── example
│           └── frontendwebapp
│               ├── app
│               ├── config
│               │   └── FrontendWebappApplication.java
│               └── domain
└── resources
    ├── application.properties
    ├── static
    └── templates
```

| ディレクトリ | 役割 |
| ---- | ---- |
| app | アプリケーション層に関するもの |
| config | Spring Bootの設定クラスを配置する。起動クラス、Webアプリケーションの設定、セキュリティ設定、データベース接続など |
| domain | ServiceクラスやRepositoryクラスなど |