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
:caption: app/web/ServiceProperties.java

package com.example.frontendwebapp.app.web;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

///////////////////////////////////////////////////////////////////////
// @ConfigurationProperties を利用することで、application.ymlの値を取得できる
//  - prefix = "service"をしていることで、「service」階層を指定
//  - 変数String dns を宣言することで、service階層配下のdnsフィールドを取得
// ========== application.yml ==========
// service:
//     dns: http://xxxx.com ←private String dns; に格納される
//     username: Taro
//     pw: hogehoge
// =====================================
///////////////////////////////////////////////////////////////////////

@Component
@ConfigurationProperties(prefix = "service")
public class ServiceProperties {

    private String dns;

    public String getDns(){
        return dns;
    }
}

```

#### 2-3. MvcConfig.javaでgetDnsで取得した基本URIを設定する

```{code-block} java
:caption: app/web/ServiceProperties.java

package com.example.frontendwebapp.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestOperations;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import com.example.frontendwebapp.app.web.ServiceProperties;

@Configuration
@ComponentScan("com.example.frontendwebapp.app.web")    //Controllerクラスは別ディレクトリなので読み込んであげる
public class MvcConfig implements WebMvcConfigurer{
    
    // backendを呼び出すときの基本URIをServicePropertiesから取得する
    // つまり、「/backend/items」へリクエストを送信するときに
    // getDns()メソッドで取得した基本URIを設定して「http://xxxx.com/backend/items」へリクエストを送信する
    @Autowired
    ServiceProperties properties;

    @Bean
    public RestOperations restOperations(RestTemplateBuilder restTemplateBuilder){
        return restTemplateBuilder.rootUri(properties.getDns()).build();
    }
}
```




