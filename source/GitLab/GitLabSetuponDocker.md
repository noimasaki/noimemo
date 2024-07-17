# コンテナでGitlabを起動する
GitLab Community Edition（CE版はMITライセンス、EE版は商用ライセンス）をコンテナで利用できるようにする。

[公式サイト](https://docs.gitlab.com/ee/install/docker.html)を参考にする。

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
    image: 'gitlab/gitlab-ce:latest'
	container_name: gitlab
    restart: always
    hostname: 'gitlab.example.com'
    environment:
      GITLAB_OMNIBUS_CONFIG: |
		# Add any other gitlab.rb configuration here, each on its own line
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
    image: gitlab/gitlab-runner:latest
    container_name: gitlab_runner
    restart: always
    volumes:
      - /srv/gitlab-runner/config:/etc/gitlab-runner
      - /var/run/docker.sock:/var/run/docker.sock
```


## 3. コンテナ作成
```
cd /srv/gitlab/
docker-compose up -d
```

構築中のログは、`docker logs -f gitlab-web-1`で確認できる。

STATUSがstartingはまだコンテナの構築中。STATUSはhealthyになったら構築完了
```


```
## 