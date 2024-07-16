# Ansible+Serverspecコンテナを作成
サーバ構築およびパラメータ確認を目的とした自動化コンテナを作成する。

## 1. podmanインストール
rootでpodmanをインストールする。
```
dnf install -y podman
```


## 2. TERAIAコンテナを作成する
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

## 鍵生成・登録
```
# Ansibleサーバで公開鍵・秘密鍵を作成
chmod 700 /TERA_IA/key
ssh-keygen -t rsa -f /TERA_IA/key/setup-key -N ""

# Ansibleサーバから構築対象サーバに公開鍵を転送
ssh-copy-id -i /TERA_IA/key/setup-key.pub cloud-user@【構築対象サーバ】

# Ansibleサーバ自身にも公開鍵を登録
cat /TERA_IA/key/setup-key.pub >> /root/.ssh/authorized_keys
```


## /etc/hosts編集
名前解決したいサーバを追記する。
```
172.19.232.90   Playbook-rhel
```



## コンテナ起動
ルートユーザで実行する。
```
# インポート
podman load -i teraia_container.tar

podman run --rm -it -v /TERA_IA:/TERA_IA:Z teraia-container
```

## hostsファイル生成
```
cd /TERA_IA/playbooks/RHEL8
/opt/coralis_tools/ansible/sdf2ansiblefiles.sh ./sdfs/conf/ENV.conf
```

## 実行
```
cd /var/TERA_IA/playbooks/RHEL8

# 構文チェック
ansible-playbook -i ./inventories/hosts ./site.yml --check

# 実行
ansible-playbook -i ./inventories/hosts ./site.yml
```


## host.listの作成



## Serverspecによる試験


```{code-block}
:caption: 失敗したとき

[root@480fedb352f6 spec_files]# rake spec
#############################################################################
   Target host: Playbook-rhel
#############################################################################
/usr/bin/ruby -I/usr/local/share/gems/gems/rspec-support-3.13.1/lib:/usr/local/share/gems/gems/rspec-core-3.13.0/lib /usr/local/share/gems/gems/rspec-core-3.13.0/exe/rspec ./spec/Linux/code/spec_file/begin_test_spec.rb
=============================================================================
 Test target: directories
=============================================================================

<<< File_ATTRIBUTE >>>
  File "/root/work"
    is expected to be owned by "root" (FAILED - 1)

<<< File_ATTRIBUTE >>>
  File "/root/work"
    is expected to be grouped into "root" (FAILED - 2)

<<< File_ATTRIBUTE >>>
  File "/root/work"
    is expected to be mode 755 (FAILED - 3)

<<< File_ATTRIBUTE >>>
  File "/root/work2"
    is expected to be owned by "root" (FAILED - 4)

<<< File_ATTRIBUTE >>>
  File "/root/work2"
    is expected to be grouped into "root" (FAILED - 5)

<<< File_ATTRIBUTE >>>
  File "/root/work2"
    is expected to be mode 700 (FAILED - 6)

Failures:

  1) <<< File_ATTRIBUTE >>> File "/root/work" is expected to be owned by "root"
     On host `Playbook-rhel'
     Failure/Error: it { should be_owned_by     value } if key == 'owner'
       expected `File "/root/work".owned_by?("root")` to be truthy, got false
       /bin/sh -c stat\ -c\ \%U\ /root/work\ \|\ grep\ --\ \\\^root\\\$

     # ./spec/Linux/code/test_pattern/common.rb:169:in `block (3 levels) in File_ATTRIBUTE'

  2) <<< File_ATTRIBUTE >>> File "/root/work" is expected to be grouped into "root"
     On host `Playbook-rhel'
     Failure/Error: it { should be_grouped_into value } if key == 'group'
       expected `File "/root/work".grouped_into?("root")` to be truthy, got false
       /bin/sh -c stat\ -c\ \%G\ /root/work\ \|\ grep\ --\ \\\^root\\\$

     # ./spec/Linux/code/test_pattern/common.rb:170:in `block (3 levels) in File_ATTRIBUTE'

  3) <<< File_ATTRIBUTE >>> File "/root/work" is expected to be mode 755
     On host `Playbook-rhel'
     Failure/Error: it { should be_mode         value } if key == 'mode'
       expected `File "/root/work".mode?(755)` to be truthy, got false
       /bin/sh -c stat\ -c\ \%a\ /root/work\ \|\ grep\ --\ \\\^755\\\$

     # ./spec/Linux/code/test_pattern/common.rb:171:in `block (3 levels) in File_ATTRIBUTE'

  4) <<< File_ATTRIBUTE >>> File "/root/work2" is expected to be owned by "root"
     On host `Playbook-rhel'
     Failure/Error: it { should be_owned_by     value } if key == 'owner'
       expected `File "/root/work2".owned_by?("root")` to be truthy, got false
       /bin/sh -c stat\ -c\ \%U\ /root/work2\ \|\ grep\ --\ \\\^root\\\$

     # ./spec/Linux/code/test_pattern/common.rb:169:in `block (3 levels) in File_ATTRIBUTE'

  5) <<< File_ATTRIBUTE >>> File "/root/work2" is expected to be grouped into "root"
     On host `Playbook-rhel'
     Failure/Error: it { should be_grouped_into value } if key == 'group'
       expected `File "/root/work2".grouped_into?("root")` to be truthy, got false
       /bin/sh -c stat\ -c\ \%G\ /root/work2\ \|\ grep\ --\ \\\^root\\\$

     # ./spec/Linux/code/test_pattern/common.rb:170:in `block (3 levels) in File_ATTRIBUTE'

  6) <<< File_ATTRIBUTE >>> File "/root/work2" is expected to be mode 700
     On host `Playbook-rhel'
     Failure/Error: it { should be_mode         value } if key == 'mode'
       expected `File "/root/work2".mode?(700)` to be truthy, got false
       /bin/sh -c stat\ -c\ \%a\ /root/work2\ \|\ grep\ --\ \\\^700\\\$

     # ./spec/Linux/code/test_pattern/common.rb:171:in `block (3 levels) in File_ATTRIBUTE'

Finished in 2.1 seconds (files took 0.68981 seconds to load)
6 examples, 6 failures

Failed examples:

rspec './spec/Linux/code/test_pattern/common.rb[1:1:1]' # <<< File_ATTRIBUTE >>> File "/root/work" is expected to be owned by "root"
rspec './spec/Linux/code/test_pattern/common.rb[2:1:1]' # <<< File_ATTRIBUTE >>> File "/root/work" is expected to be grouped into "root"
rspec './spec/Linux/code/test_pattern/common.rb[3:1:1]' # <<< File_ATTRIBUTE >>> File "/root/work" is expected to be mode 755
rspec './spec/Linux/code/test_pattern/common.rb[4:1:1]' # <<< File_ATTRIBUTE >>> File "/root/work2" is expected to be owned by "root"
rspec './spec/Linux/code/test_pattern/common.rb[5:1:1]' # <<< File_ATTRIBUTE >>> File "/root/work2" is expected to be grouped into "root"
rspec './spec/Linux/code/test_pattern/common.rb[6:1:1]' # <<< File_ATTRIBUTE >>> File "/root/work2" is expected to be mode 700
```

```{code-block}
:caption: 成功したとき

[root@480fedb352f6 spec_files]# rake spec
#############################################################################
   Target host: Playbook-rhel
#############################################################################
/usr/bin/ruby -I/usr/local/share/gems/gems/rspec-support-3.13.1/lib:/usr/local/share/gems/gems/rspec-core-3.13.0/lib /usr/local/share/gems                                                                                                          /gems/rspec-core-3.13.0/exe/rspec ./spec/Linux/code/spec_file/begin_test_spec.rb
=============================================================================
 Test target: directories
=============================================================================

<<< File_ATTRIBUTE >>>
  File "/root/work"
    is expected to be owned by "root"

<<< File_ATTRIBUTE >>>
  File "/root/work"
    is expected to be grouped into "root"

<<< File_ATTRIBUTE >>>
  File "/root/work"
    is expected to be mode 755

<<< File_ATTRIBUTE >>>
  File "/root/work2"
    is expected to be owned by "root"

<<< File_ATTRIBUTE >>>
  File "/root/work2"
    is expected to be grouped into "root"

<<< File_ATTRIBUTE >>>
  File "/root/work2"
    is expected to be mode 700

Finished in 1.98 seconds (files took 0.64302 seconds to load)
6 examples, 0 failures
```

