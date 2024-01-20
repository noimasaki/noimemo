# マイクロサービス作成② （AWS環境の構築）
## 実施すること
AWS上でコンテナが動作する環境を構築する。まずは基本的な構成を作成して動作できることを目指す。

![aws](_static/SpringMicroservice_2/aws.drawio.svg)

## 作成の流れ
1. VPC作成
2. ALB作成
3. コンテナのDockerHubへのプッシュ
4. ECSクラスタ作成
5. ECSタスク定義
6. ECSサービス実行

## 1. VPC作成
### 1-1. VPC
1. VPC作成
  - 作成するリソース：VPCのみ
  - 名前タグ：ma-noim-vpc
  - IPv4 CIDR：10.2.76.0/24
設定できたら「VPCを作成」

2. サブネット作成 [VPC > サブネット > サブネットを作成]
  - VPC ID：ma-noim-vpc
その他の設定は以下のように4つのサブネットに分割する

| サブネット名 | アベイラビリティーゾーン | IPv4 subnet CIDR block |
| ---- | ---- | ---- |
| ma-noim-vpc-subnet-public1 | ap-northeast-1a | 10.2.76.0/26 |
| ma-noim-vpc-subnet-public2 | ap-northeast-1c | 10.2.76.64/26 |
| ma-noim-vpc-subnet-private1 | ap-northeast-1a | 10.2.76.128/26 |
| ma-noim-vpc-subnet-private2 | ap-northeast-1c | 10.2.76.192/26 |