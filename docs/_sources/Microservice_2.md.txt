# マイクロサービス作成② （AWS環境の構築）
## 実施すること
作成したSpringBootアプリケーションを含めたコンテナをAWS上で動作させる。

アーキテクチャは以下のように作成する。





![aws](_static/SpringMicroservice_2/aws.drawio.svg)

## 作成の流れ
1. VPC作成
2. ALB作成
3. コンテナのDockerHubへのプッシュ
4. ECSクラスタ作成
5. ECSタスク定義
6. ECSサービス実行

## 1. VPC作成
### 1-1. VPC作成 [VPC > お使いのVPC > VPC を作成]
  - 作成するリソース：VPCのみ
  - 名前タグ：ma-noim-vpc
  - IPv4 CIDR：10.2.76.0/24
設定できたら「VPCを作成」

### 1-2. サブネット作成 [VPC > サブネット > サブネットを作成]
  - VPC ID：ma-noim-vpc
その他の設定は以下のように4つのサブネットに分割する

| サブネット名 | アベイラビリティーゾーン | IPv4 subnet CIDR block |
| ---- | ---- | ---- |
| ma-noim-vpc-subnet-public1 | ap-northeast-1a | 10.2.76.0/26 |
| ma-noim-vpc-subnet-public2 | ap-northeast-1c | 10.2.76.64/26 |
| ma-noim-vpc-subnet-private1 | ap-northeast-1a | 10.2.76.128/26 |
| ma-noim-vpc-subnet-private2 | ap-northeast-1c | 10.2.76.192/26 |

### 1-3. ルートテーブル作成 [VPC > ルートテーブル > ルートテーブルを作成]
ここまで作成したサブネットはデフォルトのルートテーブルに接続されている。

![default_rtb](_static/SpringMicroservice_2/default_rtb.png)

デフォルトのルートテーブルはNATゲートウェイのルーティングが有効化されているプライベートサブネット向けであるため、インターネットからアクセス可能としたいパブリックサブネットは、インターネットゲーウェイのルーティングが有効化されているカスタムルートテーブルに紐づける必要がある。

まずは、カスタムルートテーブルを作成する。
  - 名前：ma-noim-vpc-rtb-pub
  - VPC：ma-noim-vpc

カスタムルートテーブルをサブネットに紐づける。[VPC > ルートテーブル > rtb-ID > サブネットの関連付けを編集]
  - 関連付け対象①：ma-noim-vpc-subnet-public1
  - 関連付け対象②：ma-noim-vpc-subnet-public2

### 1-4. インターネットゲートウェイ作成 [VPC > インターネットゲートウェイ > インターネットゲートウェイの作成]
カスタムルートテーブルのデフォルトゲートウェイにインターネットゲートウェイを紐づけるために、インターネットゲートウェイを作成する
  - 名前：ma-noim-vpc-igw

作成したigwをVPCにアタッチする[VPC > インターネットゲートウェイ > VPC にアタッチ (インターネットゲートウェイID)]
  - 使用可能なVPC：ma-noim-vpc

### 1-5. カスタムルートテーブルにルートを追加 [VPC > ルートテーブル > rtb-ID > ルートを編集]
igwの作成ができたら、ルートテーブルの設定を開き、ルートを追加する
  - 送信先：0.0.0.0/0
  - ターゲット：ma-noim-vpc-igwのインターネットゲートウェイID


## 2. ALB作成
インターネットからフロントエンドへのアクセスだけでなく、フロントエンドからバックエンドへのアクセスもHTTPを利用した構成であるため、ロードバランサにはアプリケーションロードバランサ（ALB）を利用する。また、パブリックサブネットへのアクセスとプライベートサブネットへのアクセスはアクセス元を制御する（プライベートサブネットへはインターネットからの通信を遮断）必要があるので、publicとprivateはそれぞれ別のALBを用意して、セキュリティグループにてアクセス制御を実施する。

### 2-1. セキュリティグループ作成
それぞれのALBに適用するセキュリティグループ（通信制御）を作成しておく

[EC2 > セキュリティグループ > セキュリティグループを作成]

|  | パブリックサブネット | プライベートサブネット |
| ---- | ---- | ---- |
| セキュリティグループ名 | ma-noim-sg-pub | ma-noim-sg-pri |
| VPC | ma-noim-vpc | ma-noim-vpc |
| インバウンドルール（プロトコル）| HTTP/80 | HTTP/80 |
| インバウンドルール（送信元） | 0.0.0.0/0 | 10.2.76.0/24 |


### 2-2. ターゲットグループ
[EC2 > ターゲットグループ > ターゲットグループの作成]

ECSで起動タイプでFargateを利用する場合はターゲットタイプは「IPアドレス」。起動タイプをインスタンスとするならば「インスタンス」。

|  | パブリックサブネット | プライベートサブネット |
| ---- | ---- | ---- |
| ターゲットタイプ | IPアドレス | IPアドレス |
| ターゲットグループ名 | ma-noim-tg-pub | ma-noim-tg-pri |
| プロトコル/ポート| HTTP/80 | HTTP/80 |
| VPC | ma-noim-vpc | ma-noim-vpc |
| ヘルスチェク | /index.html | /index.html |

ターゲットを登録する画面は、後にECSサービスを作成する時に指定するので空欄で作成する。

### 2-3. ALB作成
[EC2 > ロードバランサー > ロードバランサータイプの比較と選択]

|  | パブリックサブネット | プライベートサブネット |
| ---- | ---- | ---- |
| ロードバランサータイプ | Application Load Balancer | Application Load Balancer |
| ロードバランサー名 | ma-noim-alb-pub | ma-noim-alb-pri |
| スキーム | インターネット向け | 内部 |
| VPC | ma-noim-vpc | ma-noim-vpc |
| マッピング | ma-noim-vpc-subnet-public1, ma-noim-vpc-subnet-public2 | ma-noim-vpc-subnet-private1, ma-noim-vpc-subnet-private2 |
| セキュリティグループ | ma-noim-sg-pub | ma-noim-sg-pri |
| リスナー（プロトコル/ポート）| HTTP/80 | HTTP/80 |
| 転送先 | ma-noim-tg-pub | ma-noim-tg-pri |

### 2-4. パスベースのルーティング設定
★よくわからず★

https://news.mynavi.jp/techplus/article/techp4359/


## 4. ECSクラスタ作成
[Amazon Elastic Container Service > クラスターの作成]

 - クラスタ名：ma-noim-ecs-cluster-pub
 - インフラストラクチャ：AWS Fargate

## 5. ECSタスク定義
[Amazon Elastic Container Service > 新しいタスク定義の作成]

 - タスク定義ファミリー：ma-noim-ecs-task-frontend
 - 起動タイプ：AWS Fargate
 - タスクロール：なし（AWSのサービスを利用する場合は適したIAMロールを作成して適用）
 - コンテナ 名前：frontend-webapp
 - コンテナ イメージ：noimasaki/frontend-webapp
 - コンテナ ポートマッピング：8080
 - ログ収集：有効


## 6. ECSサービス定義
[Amazon Elastic Container Service > クラスター > クラスターID > サービスの作成]

 - アプリケーションタイプ：サービス
 - ファミリー：ma-noim-ecs-task-frontend
 - サービス名：ma-noim-ecs-service-pub
 - VPC：ma-noim-vpc
 - サブネット：ma-noim-vpc-subnet-public1, ma-noim-vpc-subnet-public2
 - セキュリティグループ：ma-noim-sg-pub
 - パブリックIP：有効
 - ロードバランサー：ma-noim-alb-pub
 - リスナー：80:HTTP