SpringBootによるアプリ開発
##############################

1. ディレクトリ構造
======================
`レイヤ化 <https://terasolunaorg.github.io/guideline/current/ja/Overview/ApplicationLayering.html>`_ を参照してディレクトリ構造を整理する。

.. code-block:: bash

    SpringMicroservice/src/main
    ├── java/com/example
    │   └── Microservice_x
    │       ├── Application.java          # 起動クラス
    │       ├── app                       # アプリケーション層：クライアントとのデータ入出力
    │       │   └── Controller.java       #   - コントローラ
    │       ├── domain                    # ドメイン層：ビジネスルールを実行
    │       │   ├── Model.java            #   - ドメインオブジェクト
    │       │   ├── Repository.java       #   - DBへのCRUD処理（IFのみ）
    │       │   └── Service.java          #   - サービスクラス
    │       ├── repository                # リポジトリ層：外部との送受信の実態
    │       │   └── RepositoryImpl.java   #   - DBへのCRUD処理実態
    │       ├── config                    # Spring設定クラスを配置
    │       │   ├── SecurityConfig.java
    │       │   └── WebClientConfig.java
    │       └── aspect                    # AOP関連のクラスを配置
    │           └── Logging.java          #   - ログ
    └── resources
        ├── application.yml     # アプリケーション設定ファイル
        ├── static              # 静的リソース（CSS、JavaScript、画像など）
        └── templates           # テンプレート（html）
            ├── home.html
            ├── login.html
            └── logout.html


x. AOP
=======================

