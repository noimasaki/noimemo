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


