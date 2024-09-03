# GitLabRunnerによるCICD
GitLab Runnerとは、GitLab CI/CD（継続的インテグレーション/継続的デリバリー）パイプラインでジョブを実行するための軽量なエージェントでる。
コードのビルド、テスト、デプロイなどのタスクを自動化するために使われる。GitLab CI/CDで定義されたジョブを受け取り、そのジョブを指定された環境（例えばDockerコンテナや仮想マシン）で実行する。

## 目指すもの
![Arch.drawio.svg](./GitLabRunner/Arch.drawio.svg)

- GitLabのリポジトリのソースコードをビルドして、同一サーバ上のPodmanにデプロイ
- ソースコードのビルド環境はGコンテナ（docker executoを利用する）

## 1. GitLab Runnerインストール
```bash
# リポジトリ有効化
curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.rpm.sh" | sudo bash
# インストール
sudo dnf install gitlab-runner
```

任意のホスト名で、自サーバを名前解決できるように、`/etc/hosts`に追記
```bash
127.0.0.1   gitlab.noimk.com
```


