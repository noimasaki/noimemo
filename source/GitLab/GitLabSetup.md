# GitLabセットアップ
GitLab CEをインターネットにつながる環境にインストールする。
OSはRHEL9を前提とする。

## 1. GitLabリポジトリを有効化
```
curl "https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.rpm.sh" | sudo bash
```

## 2. インストール
```
dnf install gitlab-ce
```

## 3. セットアップ
事前に`EXTERNAL_URL`の環境変数を設定していない場合は自動で起動しない。設定ファイルを編集後に再構成する必要がある。

```bash
vi /etc/gitlab/gitlab.rb
```

最低限以下の設定を実施する。
| 項目         | 設定値                    |
| ------------ | ------------------------- |
| external_url | 'http://vscode.noimk.com' |

設定ファイルの編集が完了したら設定を再構築する。

```bash
gitlab-ctl reconfigure
```


## 参考：アンインストール
- [https://gitlab-docs.creationline.com/omnibus/installation/#linux%E3%83%91%E3%83%83%E3%82%B1%E3%83%BC%E3%82%B8omnibus%E3%81%AE%E3%82%A2%E3%83%B3%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB](https://gitlab-docs.creationline.com/omnibus/installation/#linux%E3%83%91%E3%83%83%E3%82%B1%E3%83%BC%E3%82%B8omnibus%E3%81%AE%E3%82%A2%E3%83%B3%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)


```bash
gitlab-ctl stop
 sudo systemctl stop gitlab-runsvdir
 sudo systemctl disable gitlab-runsvdir
 sudo rm /usr/lib/systemd/system/gitlab-runsvdir.service
 sudo systemctl daemon-reload
 sudo systemctl reset-failed
  sudo gitlab-ctl cleanse && sudo rm -r /opt/gitlab
```