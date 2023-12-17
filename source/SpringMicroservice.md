# SpringBootでマイクロサービス
以下を参考に、マイクロサービスを作成する。
- [https://news.mynavi.jp/techplus/article/techp5131/](https://news.mynavi.jp/techplus/article/techp5131/)
- [https://github.com/debugroom/mynavi-sample-aws-microservice/tree/feature_1-frontend-webapp](https://github.com/debugroom/mynavi-sample-aws-microservice/tree/feature_1-frontend-webapp)

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

なお、設定クラスは`@Configuration`アノテーションを付与することで、設定クラスとして読み込まれる。
![config dir](_static/SpringMicroservice/1_configdir.png)

## 3. `SecurityConfig.java`作成
SpringSecurity設定クラスを作成する。



------------------------

# 1. `login.html`を作成
`resources/templates`にログインページを作成

# 2. `SecurityConfig.java`を作成
```
package com.example.frontendwebapp.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {
    
    @Bean   // 戻り値がBeanに登録される。BeanとはDIコンテナに登録されるオブジェクトのこと。結果として任意の場所でAutowiredできる。
    protected SecurityFilterChain configure(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests((requests) -> requests
            .requestMatchers("/login/*").permitAll()    // "/login"は認証不要
            .anyRequest().authenticated()   // その他のリクエストは認証が必要
            )
            .formLogin((form) -> form    // 認証方式はformログイン
            .loginPage("/login")    // 認証ページは"/login"
            .permitAll()
            )
            .logout((logout) -> logout.permitAll());    // ログアウト機能を有効化し、すべてのユーザがログアウト可能

        return http.build();
    }

    // @Bean
    // public PasswordEncoder passwordEncoder() {
    //     return new Pbkdf2PasswordEncoder();
    // }

    // userDetailsServiceやpasswordEncoderについてはAutowiredできるものがあれば、自動でAutowiredして利用してくれるので不要。
    // userDetailsServiceはCustomUserDetailsServiceの中で@ServiceアノテーションをつけてServiceとしてDIコンテナに登録しているので、Springは勝手に読み取って使ってくれる
    // passwordEncoderについても同様に、PasswordEncoderConfigの中で@BeanをつけてDIコンテナに登録しているので、Pbkdf2PasswordEncoderを自動で使ってくれる


}

```