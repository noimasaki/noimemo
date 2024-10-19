# SpringBoot プロジェクトセットアップ

## 1. SpringInitializer

- Spring Web: RESTful Web アプリケーションを作成する際に使用。
- Spring Data JPA: データベース操作に JPA を使用。
- Spring Security: 認証・認可を提供。
- Spring Boot DevTools: 開発支援ツール。自動リロードなどが可能。
- MySQL/PostgreSQL Driver: 外部データベース接続用のドライバ。

## 2. ディレクトリ変更

```bash
├── src
│   ├── main
│   │   ├── java
│   │   │   └── com
│   │   │       └── noimk
│   │   │           └── todo
│   │   │               ├── TodoApplication.java
│   │   │               ├── app
│   │   │               ├── config
│   │   │               └── domain
│   │   │                   ├── model
│   │   │                   ├── repository
│   │   │                   └── service
│   │   └── resources
│   │       ├── application.properties
│   │       ├── static
│   │       └── templates
```
