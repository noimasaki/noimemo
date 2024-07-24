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

ローカルリポジトリ作成
```
# createrepoツールインストール
dnf install createrepo

# ローカルリポジトリ作成
cd ./gitlab_offline/
createrepo .
```

```{code-block}
:caption: /etc/yum.repos.d/local.repo

[local]
name=Local Repository
baseurl=file:///tmp/gitlab_offline
enabled=1
gpgcheck=0
```

リポジトリキャッシュ更新
```
dnf clean all
dnf makecache
```

インストール
```
dnf install -y gitlab-ce
```

## 3. 起動
まず、初期ユーザであるrootユーザのパスワードを設定する
```{code-block}
:caption: /etc/gitlab/gitlab.rb

[修正前①]
# gitlab_rails['initial_root_password'] = "password"

[修正後①]
gitlab_rails['initial_root_password'] = "password"

[修正前②]
external_url 'http://gitlab.example.com'

[修正後②]
external_url 'http://【自サーバのIP】`
```

その後、gitlab-ce再設定&再起動
```
gitlab-ctl reconfigure
gitlab-ctl restart
```