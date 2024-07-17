# コンテナでGitlabを起動する
GitLab Community Edition（CE版はMITライセンス、EE版は商用ライセンス）をコンテナで利用できるようにする。

[公式サイト](https://docs.gitlab.com/ee/install/docker.html)を参考にする。

## 前提条件
- podmanがインストールされていること（`dnf install podman`）
- podman-composeがインストールされていること（`dnf install podman-compose`）

## 1. マウント用ディレクトリ作成
```
# GitLab用
mkdir /srv/gitlab

# GitLabRunner用
mkdir /srv/gitlab-runner
```

## 2. docker-compose.yml作成
```
vi /srv/gitlab/docker-compose.yml
```

要件は
- `gitlab-ce`で構築
- `GITLAB_OMNIBUS_CONFIG`で設定を変更することができる
- 22番ポートはホストOSのsshdで使われているので2224ポートに変更
  
```{code-block}
:caption: /srv/gitlab/docker-compose.yml

version: '3.6'
services:
  gitlab:
    image: 'docker.io/gitlab/gitlab-ce:latest'
    restart: always
    hostname: 'gitlab.example.com'
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'https://gitlab.example.com'
        gitlab_rails['gitlab_shell_ssh_port'] = 2224
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
    volumes:
      - /srv/gitlab-runner/config:/etc/gitlab-runner
      - /var/run/docker.sock:/var/run/docker.sock
```


## 3. コンテナ作成
```
cd /srv/gitlab/
podman-compose up -d
```

構築中のログは、`docker logs -f gitlab-web-1`で確認できる。

STATUSがstartingはまだコンテナの構築中。STATUSはhealthyになったら構築完了

```{code-block}
:caption: まだ構築中

CONTAINER ID  IMAGE                                  COMMAND               CREATED         STATUS                    PORTS
e76e46a7ee37  docker.io/gitlab/gitlab-ce:latest      /assets/wrapper       24 seconds ago  Up 24 seconds (starting)  （略）
3386d2c537de  docker.io/gitlab/gitlab-runner:latest  run --user=gitlab...  5 seconds ago   Up 5 seconds
```

```{code-block}
:caption: 完了

CONTAINER ID  IMAGE                                  COMMAND               CREATED        STATUS                  PORTS
e76e46a7ee37  docker.io/gitlab/gitlab-ce:latest      /assets/wrapper       3 minutes ago  Up 3 minutes (healthy)  （略）
3386d2c537de  docker.io/gitlab/gitlab-runner:latest  run --user=gitlab...  2 minutes ago  Up 2 minutes
```

## GitLabへアクセス
`https://【サーバのIPアドレス】/`でアクセス可能。ローカルから行く場合は[https://localhost/](https://localhost/)

![Login](./GitLabSetuponDocker/Login.png)


GitLabの初期ユーザ（root）のパスワードは以下のいずれかで確認できる。catしているファイルは同一
```
# ホストOS上のファイルを直アクセス
cat /srv/gitlab/config/initial_root_password

# コンテナ経由でホストOS上のファイルへアクセス
podman exec gitlab_gitlab_1 cat /etc/gitlab/initial_root_password
```



