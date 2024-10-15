# バックアップとリストア

## 1. GitLab のバックアップ方法

バックアップは`gitlab-backup`コマンドを使用します。

### 1-1. バックアップディレクトリの確認・変更

デフォルトは`/var/opt/gitlab/backups` ですが、カスタマイズすることも可能です。

```bash
sudo vi /etc/gitlab/gitlab.rb
```

```bash
gitlab_rails['backup_path'] = "/path/to/backup"
```

設定を変更した場合、GitLab を再構築します。

```bash
sudo gitlab-ctl reconfigure
```

### 1-2. バックアップ実行

```bash
sudo gitlab-backup create
```

- バックアップファイルは`<TIMESTAMP>_gitlab_backup.tar`形式で保存されます。

### 1-3. GitLab を一時停止してバックアップ（推奨）

大規模なインスタンスの場合、競合を避けるため GitLab を一時停止します。

```bash
sudo gitlab-ctl stop puma
sudo gitlab-ctl stop sidekiq
sudo gitlab-ctl status  # 動作停止を確認
sudo gitlab-backup create
sudo gitlab-ctl start
```

## 2. GitLab のリストア方法

リストアを実行するには、GitLab インスタンスが停止している必要があります。

### 2-1. GitLab 停止

```bash
sudo gitlab-ctl stop puma
sudo gitlab-ctl stop sidekiq
sudo gitlab-ctl status  # 動作停止を確認
```

### 2-2. バックアップファイルの準備

バックアップファイルを/var/opt/gitlab/backups にコピーします（必要ならば/etc/gitlab/gitlab.rb の設定に合わせたディレクトリへ）。

### 2-3. 権限の確認

リストア対象のバックアップファイルのパーミッションを確認・変更します。

```bash
sudo chmod 600 /var/opt/gitlab/backups/<TIMESTAMP>_gitlab_backup.tar
```

### 2-4. リストア実行

```bash
sudo gitlab-backup restore BACKUP=<TIMESTAMP>
```

- `<TIMESTAMP>`は、対象のバックアップファイル名に含まれるタイムスタンプ部分を指定します。

### 2-5. GitLab を再起動

リストアが完了したら GitLab を再起動します。

```bash
sudo gitlab-ctl start
sudo gitlab-ctl status  # 正常起動を確認
```

## その他

### 構成データのリストア

GitLab の `gitlab.rb` や `secrets.json` もバックアップに含めることをお勧めします。

```bash
# 設定ファイルのバックアップ
sudo cp /etc/gitlab/gitlab.rb /path/to/backup/
sudo cp /etc/gitlab/gitlab-secrets.json /path/to/backup/

# 設定ファイルのリストア
sudo cp /path/to/backup/gitlab.rb /etc/gitlab/gitlab.rb
sudo cp /path/to/backup/gitlab-secrets.json /etc/gitlab/gitlab-secrets.json
sudo gitlab-ctl reconfigure
```

### スケジュール自動化

バックアップを定期的に自動化する場合、cron を使うと便利です。

```bash
0 2 * * * /usr/bin/sudo gitlab-backup create CRON=1
```

### Synology へのバックアップ
