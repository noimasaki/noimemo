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

2. サブネット作成
  - 