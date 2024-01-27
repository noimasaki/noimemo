# マイクロサービス作成①　（ローカル環境での開発）
## 実施すること
認証認可機能と画面表示機能を持ったフロントエンドサービスと、商品情報のCRUD操作のAPIを提供するバックエンドサービスを作成する。

ユーザはブラウザからFrontendにアクセスし、認証成功後にBackendにアクセスすることができる。

![Architecture](_static/Microservice_1/architecture.drawio.svg)

## 作成の流れ
1. フロントエンド作成
2. バックエンド作成
3. BFF改修：BFF -> バックエンドへアクセス可能とする
4. コンテナ化


## 1. フロントエンド作成
### 1-1. プロジェクト作成（Spring Initializr）
- SpringBoot: 3.2.2
- GroupId: com.example（デフォルト）
- ArtifactId: frontend-webapp
- Packaging type: Jar
- Java version: 17
- dependencies: Spring Web（spring-boot-starter-web）
- dependencies: Spring Reactive Web（spring-boot-starter-webflux）
- dependencies: Spring Security（spring-boot-starter-security）
- dependencies: Thymeleaf（spring-boot-starter-thymeleaf）

### 1-2. ディレクトリ構成変更
可読性向上の為、`.java`が含まれるディレクトリを以下のように変更する。合わせて`application.yml`を作成する。
```bash
SpringMicroservice/frontend-webapp/src/main
├── java/com/example
│   └── frontendwebapp
│       ├── app                             # アプリケーション層
│       ├── domain                          # ドメイン層
│       ├── config                          # 各種Spring設定クラスを配置
│       └── FrontendWebappApplication.java  # 起動クラス
└── resources
    ├── application.properties  # 削除：今回は.ymlに記載
    ├── application.yml         # 新規作成：アプリケーション設定ファイル
    ├── static      # 静的リソース（CSS、JavaScript、画像など）
    └── templates   # テンプレート（html）
```

SpringBootでは`@Controller`や`@Service`がついたクラスを自動で認識する。しかし、起動クラスが配置されたディレクトリ配下のみが認識対象である。例えば、config配下に起動クラスを配置した場合には`@ComponentScan`を利用して、スキャン対象のディレクトリを明示的に指定する必要がある。


### 1-3. `.html`作成
フロントエンドは画面を生成してクライアントに返す役割があるため、各種htmlを作成する。画面作成にあたって、Thymeleafを利用する。

ログインページ
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

ログイン後に表示されるホームページ
```{code-block} html
:caption: resources/templates/home.html

<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <title>Welcomeページ</title>
</head>
<body>
    <div>Successful Login!</div>

    <ul>
        <li><a href="./items.html" th:href="@{/items}">商品一覧</a></li>
    </ul>
    <ul>
        <li><a href="./logout.html" th:href="@{/logout}">ログアウト</a></li>
    </ul>
</body>
</html>
```

ログアウトページ
```{code-block} html
:caption: resources/templates/logout.html

<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <title>ログアウトページ</title>
</head>
<body>
    <h1>Microservice WebApp Logout</h1>
    <form action="#" th:action="@{/logout}" method="post">
        <div>
            <button type="submit">ログアウト</button>
        </div>
    </form>
</body>
</html>
```

### 1-4. `frontController.java`作成
@GetMappingを利用して特定のパスへのGET時に、Thymeleafによりテンプレートから生成されたhtmlを返すコントローラを作成する。

バックエンドを呼び出す処理は後ほど追加する。

```{code-block} java
:caption: app/frontController.java

package com.example.frontendwebapp.app;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class frontController {

    // 引数なしの場合はアプリケーションのコンテキストルート
    // http://<ホスト名>:<ポート番号>/ へのGET時に呼び出される
    @GetMapping
    public String home(){
        return "home";      // home.htmlをreturn
    }

    // http://<ホスト名>:<ポート番号>/login
    @GetMapping("/login")
    public String login(){
        return "login";     // login.htmlをreturn
    }

    // http://<ホスト名>:<ポート番号>/logout
    @GetMapping("/logout")
    public String logout(){
        return "logout";    // logout.htmlをreturn
    }

}
```



### 1-6. `SecurityConfig.java`作成
SpringSecurityの挙動をカスタムする

```{code-block} java
:caption: config/SecurityConfig.java

package com.example.frontendwebapp.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {
    
    // 戻り値がBeanに登録される。BeanとはDIコンテナに登録されるオブジェクトのこと。結果として任意の場所でAutowiredできる。
    @Bean
    protected SecurityFilterChain configure(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests((requests) -> requests
            .requestMatchers("/login/*").permitAll()    // "/login"は認証不要
            .anyRequest().authenticated()               // その他のリクエストは認証が必要
            )
            .formLogin((form) -> form   // 認証方式はformログイン
            .loginPage("/login")    // 認証ページは"/login"
            .permitAll()
            )
            .logout((logout) -> logout.permitAll());    // ログアウト機能を有効化し、すべてのユーザがログアウト可能
        
            return http.build();
    }
}
```

### 1-5. `WebClientConfig.java`作成
フロントエンドからバックエンドを呼び出す時は、Spring WebFluxに内包されているHTTPクライアントである「WebClient」を利用する。

@ComponentScan("com.example.frontendwebapp.app.web")
// SpringBootの起動クラスとこのControllerクラスは別パッケージ（ディレクトリ）である為、
// ComponentScanアノテーションを利用して本パッケージをスキャン対象として
// SpringBootに通知することで、コントローラクラスが読み込まれる。★修正

```{code-block} java
:caption: config/WebClientConfig.java

package com.example.frontendwebapp.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;

import com.example.frontendwebapp.app.web.ServiceProperties;

@Configuration
public class WebClientConfig {
    // backendを呼び出すときの基本URIをServicePropertiesから取得する
    // つまり、「/backend/items」へリクエストを送信するときに
    // getDns()メソッドで取得した基本URIを設定して「http://xxxx.com/backend/items」へリクエストを送信する

    @Autowired
    ServiceProperties serviceProperties;
    
    @Bean
    public WebClient webClient(){
        return WebClient.builder()
            .baseUrl(serviceProperties.getDns())
            .build();
    }
    
}
```

### 1-7. 動作確認


## 2. バックエンド作成