# GitHub Appsトークンの発行・実装方法
本記事では以下をまとめる。
 - GitHub Appsトークンとは
 - GitHub Appsの作成・インストール方法
 - GitHub ActionsでGitHub Appsトークンを利用する方法

## GitHub Appsトークンとは
GitHub Actionsでリポジトリにpushしたいなど、ワークフローの内容によっては権限が必要な作業がある。
用途ごとの権限をGitHubAppsトークンとして発行し、ワークフローに適用してあげれば、適切な権限管理が可能となる機能である。

同様な機能として、Personal Access Tokensなどがあるが、classic扱いとなっている為、GitHub Appsトークンを利用することが望ましい。

## GitHub appsのセットアップ
### 1. GitHub Appsを作成
Organizationsではなく、個人アカウントの場合はここにアクセス

[https://github.com/settings/apps/new](https://github.com/settings/apps/new)

- GitHub Apps name(*) : グローバルに一意の名前（例えば`GitHub Apps for ユーザ名`）
- Description : 任意のDescription
- Homepage URL(*) : 適当なダミー値でもOK（例えば`https://example.com`）

Webhookは不要の

# 参考
[https://zenn.dev/tmknom/articles/github-apps-token](https://zenn.dev/tmknom/articles/github-apps-token)