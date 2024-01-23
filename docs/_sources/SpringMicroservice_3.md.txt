# マイクロサービス作成③ （アプリケーション改修）
AWS環境を作成して、その上でアプリケーションを動作させる時に、現状のアプリケーション構成では不便な部分が出てくるため、改修する。

## 実施すること
1. リッスンポートの変更
2. backendへのアクセス時のDNS設定

## 1. リッスンポートの変更
backendはこれまで8081ポートでリッスンしていたが、8080ポートに変更する。

```{code-block} yaml
:caption: src/main/resources/application.yml

server:
  servlet:
   context-path: /backend
  port: 8080
```

合わせて、Dockerコンテナビルド時も8080ポートをリッスンする。

## 2. backendへのアクセス時のDNS設定
frontendからbackendを呼ぶ場合、ALBのDNSドメインを指定してアクセスすることになるが、`.Java`の中にハードコーディングしてしまうと保守性に欠ける。

そこで、application.ymlにALBリスナーのFQDNを記載して、それをコードから呼び出すことでSpringプロジェクトにおけるAWSの設定を必要最小限に抑える。

#### 2-1. applicaion.ymlへALBのFQDNを記載
```{code-block} yaml
:captin: src/main/resources/application.yml

service:
    dns: http://internal-ma-noim-alb-pri-1918403812.ap-northeast-1.elb.amazonaws.com
```

#### 2-2. application.ymlから情報を取得するクラスを作成

```{code-block} java
:caption: app/web/ItemController.java

package com.example.frontendwebapp.app.web;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "service")
public class ServiceProperties {
    private String dns;
}
```