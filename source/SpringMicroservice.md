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
