# マイクロサービス作成③ （アプリケーション改修）
## 実施すること
アプリケーションを改修し、ログ出力を実装する。

## 作成の流れ
1. テストユーザPW固定


## 1. テストユーザPW固定
現在はSpringSecurityによるデフォルトのPWを利用しているため、起動するごとにPWが変更されてしまう。そこで、テストユーザのID/PWを固定化する。以下のように追記するだけ。

```{code-block} yaml
:caption: 【frontend-webapp】/resources/application.yml
:emphasize-lines: 4-8

service:
    backendEndpoint: http://internal-ma-noim-alb-pri-1627874572.ap-northeast-1.elb.amazonaws.com

spring:
    security:
        user:
            name: user
            password: 1qaz"WSX
```

コードを修正したらcommitして、GitHub Actionにて自動ビルドしてDockerHubへアップロードする。

その後、ECSのfrontendのサービスを更新から「新しいデプロイの強制」にチェックをつけて更新するだけ。

![update_ECS](_/static/Microservice_3/update_ECS.png)

