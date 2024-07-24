# オフライン環境下のサーバにGitLabをインストール
インターネットにつながるサーバでGitLab（CE）をインストールして、オフラインのサーバにインストールする。
OSはRHEL9を前提とする。

## 1. オンライン環境化のサーバでGitLabをダウンロード
まず、GitLabリポジトリを追加する。
```
curl --silent "https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.rpm.sh" | sudo bash
```

GitLabと依存するパッケージをすべてダウンロードする。
```
# 格納用ディレクトリ作成
mkdir gitlab_offline

# ダウンロード
dnf download --resolve --destdir=./gitlab_offline gitlab-ce

# 圧縮
tar -czvf gitlab_offline.tar.gz ./gitlab_offline/
```

圧縮された`gitlab_offline.tar.gz`を適当な方法でオフライン環境下のサーバに移動する。

## 2. オフライン環境下のサーバでGitLabをインストール
転送したファイルを展開
```
tar -xzvf gitlab_offline.tar.gz
```

インストール
```
cd ./gitlab_offline/
EXTERNAL_URL="http://gitlab.example.com" dnf install -y gitlab-ce
```

