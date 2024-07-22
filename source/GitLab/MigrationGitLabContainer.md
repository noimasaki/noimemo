# GitLabコンテナの移行
ホストAで動いているGitLabコンテナを別ホストに移動させる


## 前提
コンテナ作成時の情報から移行の要件を確認する。

```{code-block}
:caption: /srv/gitlab/docker-compose.yml

version: '3.6'
services:
  gitlab:
    image: 'docker.io/gitlab/gitlab-ce:latest'
    restart: always
    hostname: 'gitlab.example.com'
    container_name: gitlab
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'https://gitlab.example.com'
        gitlab_rails['gitlab_shell_ssh_port'] = 2224
        gitlab_rails['initial_root_password'] = '1qaz"WSX'
        gitlab_rails['locale'] = 'ja'

    ports:
      - '80:80'
      - '443:443'
      - '2224:22'
    volumes:
      - '/srv/gitlab/config:/etc/gitlab'
      - '/srv/gitlab/logs:/var/log/gitlab'
      - '/srv/gitlab/data:/var/opt/gitlab'
    shm_size: '256m'
  gitlab-runner:
    image: 'docker.io/gitlab/gitlab-runner:latest'
    restart: always
    container_name: gitlab-runner
    volumes:
      - /srv/gitlab-runner/config:/etc/gitlab-runner
      - /var/run/docker.sock:/var/run/docker.sock
```

- エクスポートするコンテナイメージは`docker.io/gitlab/gitlab-ce:latest`と`docker.io/gitlab/gitlab-runner:latest`
- データ領域はホストOS上の以下ディレクトリ
  - '/srv/gitlab/config:/etc/gitlab'
  - '/srv/gitlab/logs:/var/log/gitlab'
  - '/srv/gitlab/data:/var/opt/gitlab'
  - /srv/gitlab-runner/config:/etc/gitlab-runner


## 1. ディレクトリ・docker-compose.yml の作成
移行先の環境でdocker-compose.ymlを作成する。移行元と同じものとした。

```
# ディレクトリの作成
# GitLab用
mkdir /srv/gitlab

# GitLabRunner用
mkdir /srv/gitlab-runner
```

```{code-block}
:caption: /srv/gitlab/docker-compose.yml

version: '3.6'
services:
  gitlab:
    image: 'docker.io/gitlab/gitlab-ce:latest'
    restart: always
    hostname: 'gitlab.example.com'
    container_name: gitlab
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'https://gitlab.example.com'
        gitlab_rails['gitlab_shell_ssh_port'] = 2224
        gitlab_rails['initial_root_password'] = '1qaz"WSX'
        gitlab_rails['locale'] = 'ja'

    ports:
      - '80:80'
      - '443:443'
      - '2224:22'
    volumes:
      - '/srv/gitlab/config:/etc/gitlab'
      - '/srv/gitlab/logs:/var/log/gitlab'
      - '/srv/gitlab/data:/var/opt/gitlab'
    shm_size: '256m'
  gitlab-runner:
    image: 'docker.io/gitlab/gitlab-runner:latest'
    restart: always
    container_name: gitlab-runner
    volumes:
      - /srv/gitlab-runner/config:/etc/gitlab-runner
      - /var/run/docker.sock:/var/run/docker.sock
```

## 2. イメージのエクスポート
移行元でコンテナイメージのエクスポートをする。

```
podman save -o gitlab-ce.tar docker.io/gitlab/gitlab-ce:latest
podman save -o gitlab-runner.tar docker.io/gitlab/gitlab-runner:latest
```

```{note}
GCSにアップロードする場合
```{code-block}
# gsutilインストール【初回のみ】
curl https://sdk.cloud.google.com | bash

# シェル再起動【初回のみ】
exec -l $SHELL

# gcloud環境初期化→ログインするか聞かれるので「Y」でGCPにログインする
gcloud init

# アップロード
gsutil cp 【ファイル名】 gs://【バケット名】

```

## 3. コンテナ起動
```
# インポート
podman load -i gitlab-ce.tar
podman load -i gitlab-runner.tar

# 確認→インポートしたコンテナイメージが存在すること
podman images

# 起動
cd /svr/gitlab
podman-compose up -d
```

```{note}
podman-composeが利用できない環境であれば、以下コマンドでも起動できる。

```{code-block}
# GitLabコンテナ
podman run -d \
  --name gitlab \
  --hostname gitlab.example.com \
  -p 80:80 \
  -p 443:443 \
  -p 2224:22 \
  -v /srv/gitlab/config:/etc/gitlab:Z \
  -v /srv/gitlab/logs:/var/log/gitlab:Z \
  -v /srv/gitlab/data:/var/opt/gitlab:Z \
  --shm-size 256m \
  docker.io/gitlab/gitlab-ce:latest
```

```{note}
HTTPS化のカスタマイズ

https://zenn.dev/uchidaryo/articles/setup-gitlab-https
```
