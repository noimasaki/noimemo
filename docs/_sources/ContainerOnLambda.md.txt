# Lambdaでコンテナを動かす

コンテナイメージの作成は「Spring BootをDocker上で動かす」を参照

## 前提


## ECRへコンテナアップロード
1. AWSのコンソールからECRを開き、リポジトリを作成

![ECR](_static/ContainerOnLmbda/1_ECR.png)

リポジトリの設定は以下

- 可視性設定：プライベート
- リポジトリ名：任意

2. [AWS CLIインストール](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/getting-started-install.html)

3. AWSコンソールの`プッシュコマンドの表示`に記されたコマンドを実行する

![ECR](_static/ContainerOnLmbda/2_ECR.png)


## Lambdaへデプロイ