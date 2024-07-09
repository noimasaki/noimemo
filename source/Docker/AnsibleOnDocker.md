# Ansible+Serverspecコンテナを作成


## podmanインストール
rootでpodmanをインストールする。
```
dnf install -y podman
```


## TERAIAコンテナを作成する
ディレクトリ構成
```
TERAIA_container
├── Dockerfile
└── TERASOLUNA_IA_Core_v2.4.0.zip
```

Dockerfile
```
# ベースイメージ
FROM quay.io/centos/centos:stream9

# パッケージインストール
RUN dnf install -y epel-release && \
    dnf install -y unzip tar jq && \
    dnf install -y ansible python3-pip && \
    dnf install -y ruby ruby-devel gcc make redhat-rpm-config && \
    rm -rf /var/cashe/dnf && \
    pip3 install pywinrm && \
    gem install serverspec rake highline winrm ed25519 bcrypt_pbkdf rexml && \
    ansible-galaxy collection install ansible.windows community.windows

# ZIPファイルをコンテナ内にコピー
COPY TERASOLUNA_IA_Core_v2.4.0.zip /workdir/TERASOLUNA_IA_Core_v2.4.0.zip

# ZIPファイルを解凍し、setup.shに実行権限を付与する
RUN unzip /workdir/TERASOLUNA_IA_Core_v2.4.0.zip -d /workdir && \
    chmod +x /workdir/TERASOLUNA_IA_Core_v2.4.0/setup.sh

# setup.shを適切なディレクトリで実行する
RUN cd /workdir/TERASOLUNA_IA_Core_v2.4.0 && \
    ./setup.sh && \
    rm -rf /workdir


# コンテナを実行する際のコマンド (bashシェルを実行)
CMD ["/bin/bash"]
```

ビルド
```
# ビルド
podman build -t teraia-container .
# 確認
podman images
```

コンテナ起動（終了はCtrl+D）
```
podman run --rm -it teraia-container
```

特定のディレクトリをマウントしてコンテナ起動
```
# ディレクトリ作成
mkdir -p /tmp/TERA_IA
# 権限付与
chmod -R 777 /tmp/TERA_IA

# 起動
podman run --rm -it --userns=keep-id -v /tmp/TERA_IA:/TERA_IA:Z teraia-container
```
- `--userns=keep-id`：ホストのユーザーIDとグループIDを保持するオプション。このオプションを使用することで、ホストOSのディレクトリの所有者と同じIDをコンテナ内で使用します。
- `-v /tmp/TERA_IA:/TERA_IA:Z`：ホストの/tmp/TERA_IAディレクトリをコンテナの/TERA_IAディレクトリにマウントし、SELinuxのセキュリティコンテキストを適切に設定します。（Zオプションが必要）

コンテナイメージを保存してファイルにする。
```
# エクスポートしてファイルに保存
podman save -o teraia_container.tar localhost/teraia-container

# インポート
podman load -i teraia_container.tar
```

## GCSへのアップロード
サーバから直接ファイルをダウンロードする場合は時間を要する場合があるため、Cloud Storage等のストレージを経由する。
以下コマンドでアップロードができる。

```
gsutil cp teraia_container.tar gs://【バケット名】
```


## 資材の作成
`playbook`などの資材を集めたディレクトリを、コンテナを動作させるホストOSに以下のように作成する。

```
/var/TERA_IA/playbooks/RHEL8
├── ansible.cfg
├── base.yml
├── CHANGELOG.md
├── ENV.yml
├── inventories
│   ├── group_vars
│   ├── hosts
│   └── host_vars     // SDFファイルからansibleで解釈可能なファイルが自動生成される
│       ├── NSON_RHEL92.yml
│       └── CSC_RHEL92.yml
├── res_ansible-playbook.log
├── roles
│   └── RHEL8
│       ├── defaults
│       │   └── main.yml
│       ├── tasks     // RHEL84_original.sdfで賄えないパラメータは、playbookを作成してここに入れる
│       │   ├── anacrontab.yml
│       │   ├── cron_daily.yml
│       │   ├── cron_d.yml
│       │   ├── cron_hourly.yml
│       │   ├── crontab.yml
│       │   ├── default_target.yml
│       │   ├── directories.yml
│       │   ├── group.yml
│       │   ├── grub.yml
│       │   ├── hostname.yml
│       │   ├── hosts_file.yml
│       │   ├── interfaces.yml
│       │   ├── journald.yml
│       │   ├── kdump.yml
│       │   ├── logrotate.yml
│       │   ├── main.yml
│       │   ├── NetworkManager.yml
│       │   ├── nsswitch_conf.yml
│       │   ├── NTP.yml
│       │   ├── packages_DNF.yml
│       │   ├── packages_groups.yml
│       │   ├── PAM.yml
│       │   ├── profile.yml
│       │   ├── resolv_conf.yml
│       │   ├── rsyslog.yml
│       │   ├── selinux.yml
│       │   ├── services.yml
│       │   ├── snmpd_conf.yml
│       │   ├── snmpd.yml
│       │   ├── sshd_config.yml
│       │   ├── sudoers.yml
│       │   ├── tuned.yml
│       │   ├── user.yml
│       │   └── yum_repos.yml
│       └── templates
│           └── LOOP_TEPMLATES
│               ├── type-I.j2
│               ├── type-K2.j2
│               ├── type-K.j2
│               ├── type-L.j2
│               └── type-R.j2
├── sdfs                      // パラメータシート（SDFファイル）はここに入れる
│   ├── conf
│   │   ├── ENV.conf
│   │   ├── NSON_RHEL92.conf  // 操作対象ホストが増えた場合はここに設定ファイルを追加していく
│   │   └── CSC_RHEL92.conf
│   └── RHEL84.sdf
└── site.yml
```

