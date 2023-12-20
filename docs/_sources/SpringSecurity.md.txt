# 認証機能の実装
ここでは、マイクロサービスにおけるフロントエンドに相当する認証機能を持ったアプリケーションを作成する。

## 1. Spring Initializr
動作環境
- Java: 17
- SpringBoot: 3.2.0

dependencies
- spring-boot-starter-security
- spring-boot-starter-thymeleaf
- spring-boot-starter-web

## 2. ディレクトリ構成変更
configディレクトリを作成し、起動クラスと設定クラスをまとめて格納する。設定クラスが散らばることがないので良い。


## 3. ログイン機能の実装
### 3-1. ログインページを表示してみる
dependenciesにて`spring-boot-starter-security`を指定していれば、そのまま起動するだけでログイン・ログアウト機能が使える。

![Please sign in](./_static/SpringSecurity/1_defaultAuth.png)
- ユーザ名：`user`
- パスワード：起動ログの中に記載されている。以下のようなログが出力されている。
```
Using generated security password: 827bc10f-d2e7-426a-9bca-71a10e399f74
```

ただし、ログインしてもログイン後のページがないので、`Whitelabel Error Page`が表示されるだけ。
![Whitelabel Error Page](./_static/SpringSecurity/2_error.png)

### 3-2. `.html`作成
ログインページ、ログイン後のページを作成する。

ログインページ`resources/templates/login.html`
```
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
            <label>ユーザ名</label>
            <input type="text" name="username">
            <!-- name="username"はSecurityConfig.javaにてフィールド名指定を合わせる必要がある -->
        </div>
        <div>
            <label>パスワード</label>
            <input type="password" name="password">
            <!-- name="password"はSecurityConfig.javaにてフィールド名指定を合わせる必要がある -->
        </div>
        <div>
            <button type="submit">ログイン</button>
        </div>
    </form>
</body>
</html>
```

ログイン後のページ`resources/templates/home.html`
```
<!DOCTYPE html>
<head>
    <title>Welcomeページ</title>
</head>
<body>
    <div>Successful Login!</div>
    <div>Session Id : <span th:text="${sessionId}"></span></div>
</body>
</html>
```

### 3-3. `Controller.java`作成
`login.html`と`home.html`を表示させるコントローラを作成する

```

```

