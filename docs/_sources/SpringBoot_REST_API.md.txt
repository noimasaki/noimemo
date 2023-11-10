# SpringBootでREST API
SpringBootを利用した簡単なREST APIを作成する。

## 1. 環境構築
Visual Studio Codeを利用してSpringBootを開始する。

### 1-1. プロジェクト作成
VS Codeのコマンドパレットから新しくプロジェクトを作成
![Create Project](_static/SpringBoot_REST_API/CreatePJ.png)
- Spring Boot version: 3.15
- project language: Java
- Group Id: com.example
- Artifact Id: item
- packaging type: Jar
- Java version: 17  ※ 実行環境のJavaバージョンと合わせる必要がある
- dependencies: Spring Web

作成されたディレクトリに、`Controller`フォルダ、`Model`フォルダ、`Service`フォルダを作成する

以下のようなフォルダ構成となる
```
item           // Spring Boot プロジェクディレクトリ
├── pom.xml
├── src
│   ├── main    // Javaファイルはここに作成
│   │   └── java/com/example/item
│   │       ├── ItemApplication.java
│   │       ├── Controller  // Controllerクラス用ディレクトリ
│   │       ├── Model       // Modelクラス用ディレクトリ
│   │       └── Service     // Serviceクラス用ディレクトリ
│   └── test
└── target      // ビルドしたjarファイルはここに格納される
```
### 1-2. モデル作成
1. ItemApplication.javaと同ディレクトリにモデル（Item.java）を作成し、次のオブジェクト作成
```
    private String itemId;          //商品ID
    private String itemName;        //商品名
    private String itemCategory;    //商品カテゴリー
```

1. GetterとSetterを作成
コードを記載してももちろんOKだが、右クリックから
`ソースアクション > Generate Getters and Setters...`
を選択すると自動で作って便利

![VScode](_static/SpringBoot_REST_API/VScode1.png)
↓ GetterとSetterを作成したい対象を選択してあげると
![VScode](image.png)

3. コンストラクタを作成
こちらも`ソースアクション > Generate Constructors...`から作成すると便利


Item.java
```
package com.example.item;

public class Item {
    private String itemId;          //商品ID
    private String itemName;        //商品名
    private String itemCategory;    //商品カテゴリー

    // コンストラクタ
    public Item(String itemId, String itemName, String itemCategory) {
        this.itemId = itemId;
        this.itemName = itemName;
        this.itemCategory = itemCategory;
    }
    // GetterとSetter
    public String getItemId() {
        return itemId;
    }
    public void setItemId(String itemId) {
        this.itemId = itemId;
    }
    public String getItemName() {
        return itemName;
    }
    public void setItemName(String itemName) {
        this.itemName = itemName;
    }
    public String getItemCategory() {
        return itemCategory;
    }
    public void setItemCategory(String itemCategory) {
        this.itemCategory = itemCategory;
    }
}
```

### 1-3. コントローラ作成
1. ItemController.javaを作成
```
package com.example.item;

import java.util.Arrays;
import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ItemController {
    
    @GetMapping("/items")
    public List<Item> getAllItems() {
        List<Item> allItems = Arrays.asList(
            new Item("10001", "ネックレス", "ジュエリ"),
            new Item("10002", "パーカー", "ファッション"),
            new Item("10003", "フェイスクリーム", "ビューティ"),
            new Item("10004", "サプリメント", "ヘルス"),
            new Item("10005", "ブルーベリー", "フード")
        );
        return allItems;
    }
}
```

## 2. GET（参照）の実装
`1. 環境構築`が完了していれば、GETは実装できたことになる。

1. SpringBootを起動する
![Run SpringBoot](_static/SpringBoot_REST_API/VScode3.png)

2. ブラウザで[http://localhost:8080/items](http://localhost:8080/items)にアクセスして、JSON形式で表示されればOK
![Run SpringBoot](_static/SpringBoot_REST_API/GET_1.png)

確認できたらSpringBootは停止する



## データベース（MySQL）を利用する
![DatabBase](_static/SpringBoot_REST_API/DataBase.png)

### データベース作成
MySQL Workbenchからデータベースを作成
![Opne MySQL Workbench](_static/SpringBoot_REST_API/DB_1.png)
![Create DB](_static/SpringBoot_REST_API/DB_2.png)

### プロジェクト作成
1. VS Codeのコマンドから新しくプロジェクトを作成
![Create Project](_static/SpringBoot_REST_API/CreatePJ.png)
- Spring Boot Version : 3.1.5 （一番上のやつ）
- project language : Java
- Group 