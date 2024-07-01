# TERASOLUNA IA 構築手順

## 1. 環境構築（自動化サーバ）

rootユーザにて、下記手順を実施する。


### 1-1. Ansibleインストール
自動構築を実現するために[Ansible](https://www.redhat.com/ja/blog/updates-using-ansible-rhel-86-and-90)をインストールする

```
# インストール
dnf install ansible-core -y

# バージョン確認
ansible --version
```

```{note}
ansibleをインストールすると、依存関係に従ってpythonもインストールされる。Windowsを自動構築対象とするために、後の工程で`pywinrm`をインストールする。その際に、どのpythonバージョンに`pywinrm`を導入するかを決定するために、ansibleがどのpythonバージョンを利用するかを確認しておくこと。
```{code-block}
:caption: Python3.11が利用されている
:emphasize-lines: 8

# ansible --version
ansible [core 2.14.2]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3.11/site-packages/ansible
  ansible collection location = /root/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/bin/ansible
  python version = 3.11.2 (main, Feb 16 2023, 00:00:00) [GCC 11.3.1 20221121 (Red Hat 11.3.1-4)] (/usr/bin/python3.11)
  jinja version = 3.1.2
  libyaml = True
```


### 1-2. TERASOLUNA IA Core およびTools のインストール
TERASOLUNA IA Coreを利用するのに必要なソフトウェアをインストールする。
```
dnf install -y tar unzip jq
```

`/tmp`に資材をアップロードして、展開・スクリプト実行して、TERASOLUNA IA Coreをインストールする。
```
cd /tmp/
unzip ./TERASOLUNA_IA_Core_v2.4.0.zip 
cd ./TERASOLUNA_IA_Core_v2.4.0
    bash ./setup.sh
```

### 1-3. WindowsをAnsibleで構築する為のいろいろ
公式ドキュメントには記載されていないものの、動作させるために不足している作業が見つかったため色々実施する。

Widowsを操作する場合には、Ansible Galaxy追加モジュールと`pywinrm`をAnsibleサーバに導入する必要がある。WindowsServer側もリモートでPowerShellを受け付けられるようにWinRMを有効にする必要がある。

```{mermaid}
graph TD;
    A[Ansible Controller]
    A --> B[Ansible Galaxy Windows モジュール]
    B --> C[pywinrm Library]
    C --> D[WindowsServer_WinRM]

```

#### (a) pywinrmに関連するパッケージ収集
```{note}
pywinrmのインストールは公式ドキュメントのファイル群ではうまく動作しなかったため、別途パッケージ収集したものを利用する。
```

統クラのサーバはインターネットに出られないので、インターネットにつながる環境（今回はPythonがインストールされたセキュアFAT）でパッケージを集める。

今回集めたいパッケージを記した`requirements.txt`を以下の構成で作成する。
```
# 構成
pywinrm
└── requirements.txt

# requirements.txt
pywinrm
cryptography
cffi
charset-normalizer
```

pywinrmディレクトリにて、以下コマンドを実行してパッケージをダウンロードする。
```
pip download --platform manylinux2014_x86_64 --only-binary=:all: --python-version 311 -r requirements.txt -d pywinrm_packages
```
- `--platform manylinux2014_x86_64 --only-binary=:all:` RHEL9に適したplatformのものをダウンロード
- `--python-version 311` ansible --versionコマンドで確認したpythonバージョンに合わせる
- `-d pywinrm_packages` 指定したサブディレクトリ配下にパッケージがダウンロードされる

ダウンロードできたら、`pywinrm.zip`にしてAnsibleサーバの`/tmp/`にアップロードする。

#### (b) pywinrmのインストール
Ansibleサーバの`/tmp/`ディレクトリでrootユーザにて以下を実施する。
```
# zip展開
unzip pywinrm.zip

cd ./pywinrm/pywinrm_packages

# インストール（ansible --versionで確認したPythonバージョンに合わせる）
python3.11 -m pip install --no-index --find-links /tmp/pywinrm/pywinrm_packages/ pywinrm
```

```{note}
`No module named pip`が表示される場合は下記を実施してモジュールを追加する。

```{code-block}
python3.11 -m ensurepip
```

#### (c) 追加モジュールのダウンロード
[Ansible Galaxy](https://galaxy.ansible.com/ui/)にて、以下のコレクションをダウンロードする。
- [ansible.windows](https://galaxy.ansible.com/ui/repo/published/ansible/windows/)
- [community.windows](https://galaxy.ansible.com/ui/repo/published/community/windows/)
※ `ansible --version`でバージョンを確認して適するバージョンをダウンロードすること。

ダウンロードした`.tar.gz`をAnsibleサーバの`/tmp`にアップロードする。

#### (d) 追加モジュールのインストール
Ansibleサーバにアップロードした追加モジュールをインストールする。[参考サイト](https://tekunabe.hatenablog.jp/entry/2022/12/23/120913)
```
# インストール
ansible-galaxy collection install --offline /tmp/ansible-windows-2.4.0.tar.gz
ansible-galaxy collection install --offline /tmp/community-windows-2.2.0.tar.gz

# 確認
ansible-galaxy collection list
```

ansible-core 2.14.0 以降では、`--offline`オプションをつけることで、依存関係によるエラーでなんのコレクションが足りていないかを表示してくれるようになる。該当オプションをつけない場合はオフライン環境だとインターネット接続不可のエラーメッセージが出力されるため、トラブルシュートがしずらい。


#### (e) WinRMセットアップ
自動構築対象のWindowsServerにて、管理者権限のPowerShellで実行する。

まず、既存のHTTPリスナーがあるかを確認し、存在していれば削除する。
```
# 既存リスナー確認 -> デフォルトではHTTPとHTTPSのリスナーが存在する
winrm enumerate winrm/config/listener

# リスナー削除
winrm delete winrm/config/listener?Address=*+Transport=HTTP
```

WinRMの設定・リスナーの作成を実施する。
```
Start-Service WinRM
Set-Service WinRM -StartupType Automatic
winrm create winrm/config/listener?Address=*+Transport=HTTP
winrm set winrm/config/service/auth '@{Basic="true"}'
winrm set winrm/config/service '@{AllowUnencrypted="true"}'
```

### 1-4. Serverspecインストール
自動テストを目的にServerspecをインストールする。

```
# Rubyインストール
dnf install -y ruby ruby-devel
dnf install -y gcc make redhat-rpm-config

# Serverspecインストール
cd /tmp
unzip TERASOLUNA_IA_Serverspec_materials_20220125.zip -d ./
cd ./TERASOLUNA_IA_Serverspec_materials
gem install serverspec rake highline winrm ed25519 bcrypt_pbkdf --local
```

TERA IA公式ドキュメントではServerspecインストール作業は以上だが、実際にはrexmlが足りていない。（Ruby3.0から標準Gemから除外された）

インターネットにつながる環境から以下をダウンロードしてサーバに転送する。
- [rexml](https://rubygems.org/gems/rexml/versions/3.3.0)
- [strscan](https://rubygems.org/gems/strscan) ※rexmlインストールに必要

```
# ローカルインストール（/tmpにgemファイルを転送したとする）
gem install --local /tmp/strscan-3.1.0.gem
gem install --local /tmp/rexml-3.3.0.gem
```



## 2. Ansibleによる自動構築
rootユーザで実施する。

### 2-1. 作業ディレクトリ準備【実施済み】
```
mkdir -p /var/TERA_IA/playbooks
```

### 2-2. SSHキー作成（Linux向け）【実施済み】
```
mkdir -p /var/TERA_IA/key
chmod 700 /var/TERA_IA/key
cd /var/TERA_IA/key
ssh-keygen -t rsa -f ./setup-key -N ""
```

### 2-3. SSHキーの登録（Linux向け）【実施済み】
ansibleサーバおよび構築対象サーバにて、SSHキーを登録する
```
sudo su -
cd /tmp
cat ./setup-key.pub >> /root/.ssh/authorized_keys
```
※ansibleサーバ自身からansible操作を実行するため、ansibleサーバ自身の`authorized_keys`にも登録する。



### 2-5. サンプルplaybookを配置【実施済み】

ansibleサーバにて以下コマンドを実行して解凍する。
```
unzip /tmp/sample_ansible_rhel8-master.zip
mv -T ./sample_ansible_rhel8-master /var/TERA_IA/playbooks/RHEL8
```

同様に、WindowsServerのサンプル資材も/tmp/にアップロードする。

```
unzip /tmp/sample_ansible_windowsserver2019-master.zip
mv -T ./sample_ansible_windowsserver2019-master.zip /var/TERA_IA/playbooks/Windows
```


### 2-6. SDFファイル編集
TERASOLUNA IA Editorを作業用端末にインストールし、SDFファイルを編集する。

ディレクトリとユーザとhostsのみを編集したサンプルSDFは以下に準備した。
```{code-block}
:caption: サンプルSDFファイル（編集済み）

\\nttd-fs5.fs-bxo.nttdata.co.jp\bear2$\技術戦略担当\社員限り\FY2024\チーム別フォルダ\27_安本T\02_案件対応\03_案件別\02_TACSS2.0\99_作業\noim\04_サンプル資材加工\加工済みSDF\RHEL84.sdf
```

サンプルSDFでは`ノード名`が以下のようになっている。
- NSON_RHEL92：自動化サーバ（=ansibleサーバ）
- CSC_RHEL92：自動構築対象サーバ

これらのノード名に合わせて、ansibleサーバの下記ファイルを変更する。
```{code-block}
:caption: 変更前

# フォルダ構成
/var/TERA_IA/playbooks/RHEL8
├── sdfs
│   ├── conf
│   │   ├── ENV.conf
│   │   ├── node1.conf
│   │   ├── node2.conf
│   │   └── node3.conf
│   └── RHEL84.sdf      // デフォルトのサンプルSDFはノード名はnode1~3になっている
└── site.yml



# node1.confの中身（node2~3も同様）

#===============================================================================
# Inventory情報
#===============================================================================
_ANSIBLE_GROUP_NAME=base
_NODE_NAME=node1
_IP_ADDR=node1


#===============================================================================
# SDFファイルリスト（パスはPlaybookパスからの相対パス）
#===============================================================================
_SDF_LIST="
  sdfs/RHEL84.sdf
"
```

```{code-block}
:caption: 変更後
:emphasize-lines: 6-8,19-20

# フォルダ構成
/var/TERA_IA/playbooks/RHEL8
├── sdfs
│   ├── conf
│   │   ├── ENV.conf
│   │   ├── NSON_RHEL92.conf
│   │   └── CSC_RHEL92.conf
│   └── RHEL84.sdf      // サンプルSDFファイル（編集済み）をアップロード
└── site.yml



# NSON_RHEL92.confの中身（CSC_RHEL92.confもNODE_NAMEとIP_ADDRを変更）

#===============================================================================
# Inventory情報
#===============================================================================
_ANSIBLE_GROUP_NAME=base
_NODE_NAME=NSON_RHEL92
_IP_ADDR=NSON_RHEL92


#===============================================================================
# SDFファイルリスト（パスはPlaybookパスからの相対パス）
#===============================================================================
_SDF_LIST="
  sdfs/RHEL84.sdf
"
```

また、このままだとサンプルのplaybookで定義されているいくつかのtask（selinuxとinterfaces）が失敗するので一旦コメントアウトする。
```{code-block}
:caption: コメントアウトする
:emphasize-lines: 3-11

vi /var/TERA_IA/playbooks/RHEL8/roles/RHEL8/tasks/main.yml

# - import_tasks: "selinux.yml"
#   when:
#     - selinux['dict'] != {}
#     - selinux['list'] != {}

# - import_tasks: "interfaces.yml"
#   when:
#     - interfaces['dict'] != {}
#     - interfaces['list'] != {}
```

### 2-7. SDFからhost_varsを生成
この手順を実施することで、パラメータシート（SDF）からansibleで解釈可能なhost_varsが生成される。
```
cd /var/TERA_IA/playbooks/RHEL8
/opt/coralis_tools/ansible/sdf2ansiblefiles.sh ./sdfs/conf/ENV.conf
```

```{code-block}
:caption: 生成されたファイル
:emphasize-lines: 6-7

/var/TERA_IA/playbooks/RHEL8
├── inventories
│   ├── group_vars
│   ├── hosts
│   └── host_vars
│       ├── NSON_RHEL92.yml
│       └── CSC_RHEL92.yml
```

### 2-8. hostsファイルの編集【実施済み】
`NSON_RHEL92.conf`および`CSC_RHEL92.conf`では対象のサーバをホスト名で記載していたため、名前解決できるようにansibleサーバの`/etc/hosts`に追記してあげる。

- NSON_RHEL92：172.19.232.110
- CSC_RHEL92：172.19.232.68

### 2-9. ansibleの実行
以下を実行することで、実際の環境変更が実施される。事前に構文チェックをすることですでにSDFファイルの設定になっているところは「ok」と表示されて設定変更はされない。
```
cd /var/TERA_IA/playbooks/RHEL8

# 構文チェック
ansible-playbook -i ./inventories/hosts ./site.yml --check

# 実行
ansible-playbook -i ./inventories/hosts ./site.yml
```


## 3. Serverspecによる単体試験
Serverspecによってパラメータ確認の自動化が可能となり、SDFと実機情報が一致していることを確認できる。

本手順は`03_TERASOLUNA_IA_サンプル資材利用手順_Serverspec.pdf`に準拠して作成する。

### 3-1. 作業フォルダ準備
```
cd /var/TERA_IA
mkdir -p ./serverspec/RHEL8
```

```{note}
Ansibleの`/var/TERA_IA/playbooks/RHEL8`と構成を合わせる。

  ```{code-block}
  /var/TERA_IA/
  ├──playbooks/RHEL8
  └──serverspec/RHEL8
  
```

### 3-2. 資材アップロード
公式サイトよりダウンロードしたサンプル資材（21_サンプル資材_Ansible_Serverspec.zipの中）を/tmp/にアップロードする。


ansibleサーバにて以下コマンドを実行して解凍する。
```
cd /tmp
unzip /tmp/sample_serverspec-master.zip
mv -T ./sample_serverspec-master /var/TERA_IA/serverspec/RHEL8/spec_files
```

### 3-3. SDFから試験情報が格納されたYamlファイルを生成
```
cd /var/TERA_IA/serverspec/RHEL8/spec_files
mkdir -p ./parameter/RHEL8

# NSON_RHEL92
/opt/coralis/bin/sdf2yaml_serverspec.py -nn NSON_RHEL92 \
-i /var/TERA_IA/playbooks/RHEL8/sdfs/RHEL84.sdf -o ./parameter/RHEL8

# CSC_RHEL92
/opt/coralis/bin/sdf2yaml_serverspec.py -nn CSC_RHEL92 \
-i /var/TERA_IA/playbooks/RHEL8/sdfs/RHEL84.sdf -o ./parameter/RHEL8
```

### 3-4. host_listに試験対象ノードに関する情報を定義
以下コマンドを実行して、試験対象ノードに関する情報を記述した host_list ファイルを生成する。

```
cat << EOF > ./host_list.yml
NSON_RHEL92:
 :os_type: Linux
 :os_user: root
 :os_pass:
 :sudo_pass:
 :ssh_key: /var/TERA_IA/key/setup-key
 :software:
 - RHEL8
EOF
```

### 3-5. 試験実施

```
rake spec
```



## ansibleお試しメモ
TERASOLUNA IA（ansible）を利用したサーバ構築を試す手順メモを記す。
環境はすでに本手順にて構築済みであるので、パラメータシート相当のSDFファイルをansibleサーバにアップロードして、実機適用の流れを確認いただきたい。

### 手順１　TERASOLUNA IA Editorインストール・SDFファイル編集
SDFファイルを編集するためにTERASOLUNA IA Editorをインストールする。`10_TERASOLUNA_IA_Editor.zip`

インストールが完了したら、実際のSDFファイルを開いて、中身を確認する。
- `RHEL84.sdf`：ノード名を統クラの実機に合わせ、パラメータを最小限（ディレクトリ・ユーザ）に絞ったもの
- `RHEL84_original.sdf`：公式サンプル資材。パラメータが全量記載されている。

まずは、挙動を確認するために`RHEL84.sdf`をそのまま利用する。


### 手順２　SDFファイルのアップロード
ansibleサーバであるNSON_RHEL92に編集したSDFファイルをアップロードする。
```
/var/TERA_IA/playbooks/RHEL8
├── sdfs
│   ├── conf
│   └── RHEL84.sdf      // ここにアップロード
```

※すでに`RHEL84.sdf`はアップロード済み

### 手順３　SDFからhost_varsを生成
この手順を実施することで、パラメータシート（SDF）からansibleで解釈可能なhost_varsが生成される。
```
cd /var/TERA_IA/playbooks/RHEL8
/opt/coralis_tools/ansible/sdf2ansiblefiles.sh ./sdfs/conf/ENV.conf
```

```{code-block}
:caption: 生成されたファイル
:emphasize-lines: 6-7

/var/TERA_IA/playbooks/RHEL8
├── inventories
│   ├── group_vars
│   ├── hosts
│   └── host_vars
│       ├── NSON_RHEL92.yml
│       └── CSC_RHEL92.yml
├── sdfs
│   ├── conf
│   └── RHEL84.sdf
```

### 手順４　ansibleの実行
以下を実行することで、実際の環境変更が実施される。事前にチェックをすることですでにSDFファイルの設定になっているところは「ok」と表示されて設定変更はされない。
```
cd /var/TERA_IA/playbooks/RHEL8

# チェック（環境変更はされない）
ansible-playbook -i ./inventories/hosts ./site.yml --check

# 実行（実際の環境変更が実施される）
ansible-playbook -i ./inventories/hosts ./site.yml
```

その後、必要に応じてSDFファイルの通りに変更されているか確認すること。（serverspecで確認できるように準備中）

### 手順５　ほかのパラメータを弄ってみる
`RHEL84_original.sdf`をみながら`RHEL84.sdf`を編集し、手順2~4を繰り返すことで所望の挙動がされるかどうか確認すること。ただし、手順４のansibleの実行時は`--check`オプションを付与して事前確認すること。


### 手順６　現在執筆中のパラメータシートとの突き合わせ
ansibleを利用した構築自動化について、現在執筆中のパラメータシートと`RHEL84_original.sdf`を突き合わせて、対応していないパラメータがどれかをチェックいただきたい。対応していないパラメータが存在する場合には、playbookを作成する必要がある為、その影響度を確認したい。


## 【参考】ディレクトリ構成
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


