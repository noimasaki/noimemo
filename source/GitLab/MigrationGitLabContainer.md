# GitLabコンテナの移行
ホストAで動いているGitLabコンテナを別ホストに移動させる


## 前提
コンテナ作成時の情報から移行の要件を確認する。

```{code-block}
:caption: docker-compose.yml

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

- エクスポートするコンテナイメージは`docker.io/gitlab/gitlab-ce:latest`と`docker.io/gitlab/gitlab-runner:latest`
- データ領域はホストOS上の以下ディレクトリ
  - '/srv/gitlab/config:/etc/gitlab'
  - '/srv/gitlab/logs:/var/log/gitlab'
  - '/srv/gitlab/data:/var/opt/gitlab'
  - /srv/gitlab-runner/config:/etc/gitlab-runner
