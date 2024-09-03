# GitLabパイプライン
`.gitlab-ci.yml`の書き方をメモ

## 1. 基本 (shell execution)
GitLabリポジトリのトップディレクトリに`.gitlab-ci.yml`を作成して記述する

```bash
# 各stageの実行順序を記載
#  -> stageはjob(=タスク)をグループ化したもの
#  -> build→deployの順に実施
stages:
  - build
  - deploy

# job名
build-job:
  stage: build      # このjobをbuildステージに設定
  script:           # 実際のjobで実行するスクリプト
    - echo "Compiling the code"
    - mkdir ./build
    - echo "This is Build File!!" >> ./build/output.txt
  artifacts:        # 生成されたファイルはstage間で共有されない -> artifactsで指定されたファイルは共有できる
    paths:
      - "build/"    # buildディレクトリ配下のファイルをartifactsとして指定

# job名
deploy-job:
  stage: deploy  # このjobをdeployステージに設定
  script:
    - mv build/ public/
  artifacts:
    paths:
      - "public/"


```


## 2. エグゼキューションをpodmanにする方法
gitlab runnerがインストールされていること

まず、lingering を有効にします:
```
sudo loginctl enable-linger gitlab-runner
```

gitlabユーザにスイッチ
```
sudo -u gitlab-runner -i
```


環境変数を設定します。gitlab-runnerユーザーの.bash_profileファイルに以下の行を追加します:
```
echo 'export XDG_RUNTIME_DIR="/run/user/$UID"' >> ~/.bash_profile
echo 'export DBUS_SESSION_BUS_ADDRESS="unix:path=${XDG_RUNTIME_DIR}/bus"' >> ~/.bash_profile
```

変更を反映させるため、ログアウトして再度ログインするか、以下のコマンドを実行します:
```
source ~/.bash_profile
```

systemdユーザーインスタンスが正しく起動していることを確認します:
```
systemctl --user status
```

```
systemctl --user enable --now podman.socket
```

Podmanソケットがリッスンしていることを確認する
```
[gitlab-runner@rhel9 ~]$ systemctl --user status podman.socket
● podman.socket - Podman API Socket
     Loaded: loaded (/usr/lib/systemd/user/podman.socket; enabled; preset: disabled)
     Active: active (listening) since Mon 2024-09-02 10:51:12 JST; 52s ago
      Until: Mon 2024-09-02 10:51:12 JST; 52s ago
   Triggers: ● podman.service
       Docs: man:podman-system-service(1)
     Listen: /run/user/969/podman/podman.sock (Stream)
     CGroup: /user.slice/user-969.slice/user@969.service/app.slice/podman.socket
```


その際に、Listenに書いてあるパスをメモしておく（Runnerの登録で使用する）
```
/run/user/969/podman/podman.sock
```



dockerをexecutorとしてGitLab Runnerを登録した後に、`/etc/gitlab-runner/config.toml`を編集する

```
[[runners]]
  clone_url = "http://gitlab.noimk.com"
  [runners.docker]
    network_mode = "host"
    host = "unix:///run/user/969/podman/podman.sock"
    pull_policy = ["if-not-present"]
```

- network_mode = "host" について
docker executoを利用する上での注意点として、gitlabを`localhost`や`127.0.0.1`で指定したい場合に
コンテナのネットワークモードをデフォルトのbrigeモードだと`localhost`はそのコンテナ自身を示すものとなるため、gitlabサーバに到達できない。
そこで、`/etc/gitlab-runner/config.toml`でコンテナのネットワークモードをHostモードに指定してあげる必要がある。

- pull_policy = ["if-not-present"] について
指定のコンテナイメージがローカルにない場合にのみ、取得する




なお、`gitlab.noimk.com`を名前解決できるように`/etc/hosts`に記載する。
```
127.0.0.1   gitlab.noimk.com
```




Podmanはルートレスモードで動作するため、ユーザー名前空間を使用してコンテナを実行します。このため、/etc/subuidと/etc/subgidファイルに適切なエントリが必要です。これらのファイルは、ユーザーが使用できるUIDとGIDの範囲を定義します。

まず、これらのファイルにgitlab-runnerユーザーのエントリが存在するか確認します。以下のコマンドを実行して内容を確認します。

```
cat /etc/subuid
cat /etc/subgid
```

もしgitlab-runnerユーザーのエントリがない場合、以下のようにエントリを追加します。
```
echo 'gitlab-runner:100000:65536' | sudo tee -a /etc/subuid
echo 'gitlab-runner:100000:65536' | sudo tee -a /etc/subgid
```
これにより、gitlab-runnerユーザーに対してUIDとGIDの範囲が割り当てられます。

UIDとGIDの設定を反映させるために、以下のコマンドを実行してPodmanのシステムをマイグレーションします。
```
podman system migrate
```



## 参考
- [CI/CDを使ったアプリケーションの構築](https://gitlab-docs.creationline.com/ee/topics/build_your_application.html)
- [podman](https://gitlab-docs.creationline.com/runner/executors/docker.html#podman%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6docker%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%82%92%E5%AE%9F%E8%A1%8C%E3%81%97%E3%81%BE%E3%81%99)
-  [qiita](https://qiita.com/masa2223/items/d287a2f2b6f6a9367a51)
-  

