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
### 1-1. プロジェクト作成（Spring Initializr）
- Java: 17
- SpringBoot: 3.2.1
- dependencies: spring-boot-starter-web
- dependencies: spring-boot-starter-security
- dependencies: spring-boot-starter-thymeleaf

### 1-2. ディレクトリ構成変更
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

### 1-3. `.html`作成
ログインページ `resources/templates/login.html`

```{code-block} html
:caption: resources/templates/login.html

<!DOCTYPE html>
<!-- Thymeleafを有効化 => th:XXXX という属性を各タグに追加することで利用可能 -->
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <title>ログインページ</title>
</head>
<body>
    <h1>Microservice WebApp Login</h1>

    <!-- URLパラメータに「error」が含まれていたら、メッセージ出力 -->
    <div th:if="${param.error}">
        <p>ユーザー名もしくはパスワードが違います</p>
    </div>

    <!-- ユーザ名・PWをサーバへ送信するためのForm -->
    <!-- submitボタンが押下された時のaction（URLパス`/login`へ`post`する）※@はthのリンク記法 -->
    <!-- `action="#" はThymleafが有効化されていれば上書きされる -->
    <form action="#" th:action="@{/login}" method="post">
        <div>
            <label for="usernameInput">ユーザ名</label>
            <input type="text" id="usernameInput" name="username">
            <!-- name="username"はSecurityConfig.javaにてフィールド名指定を合わせる必要がある -->
        </div>
        <div>
            <label for="passwordInput">パスワード</label>
            <input type="password" id="passwordInput" name="password">
            <!-- name="password"はSecurityConfig.javaにてフィールド名指定を合わせる必要がある -->
        </div>
        <div>
            <button type="submit">ログイン</button>
        </div>
    </form>
</body>
</html>
```