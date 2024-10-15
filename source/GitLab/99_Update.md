# アップデート

GitLab のアップデート方法を記述する。

## 前提

- OS: RHEL9
- パッケージ：コミュニティ版（gitlab-ce）
- GitLab インストール方法：dnf install

## アップデート手順

### 1. GitLab リポジトリの有効化

インストール時にすでに有効化されていれば実施しなくても良い。

```bash
curl "https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.rpm.sh" | sudo bash
```

### 2. アップデートの実施

```bash
sudo dnf install gitlab-ce
```

## トラブルシュート

### (1) 前提バージョンの不足

以下のようなエラーが発生する場合がある。

```bash
[root@rhel9 ~]# dnf install gitlab-ce
サブスクリプション管理リポジトリーを更新しています。
gitlab_gitlab-ce                                                                                                      283  B/s | 862  B     00:03
gitlab_gitlab-ce-source                                                                                               399  B/s | 862  B     00:02
gitlab_gitlab-ee                                                                                                      1.9 kB/s | 1.0 kB     00:00
gitlab_gitlab-ee-source                                                                                               973  B/s | 951  B     00:00
runner_gitlab-runner                                                                                                  287  B/s | 862  B     00:03
runner_gitlab-runner-source                                                                                           341  B/s | 862  B     00:02
パッケージ gitlab-ce-17.2.2-ce.0.el9.x86_64 は既にインストールされています。
依存関係が解決しました。
======================================================================================================================================================
 パッケージ                       アーキテクチャー              バージョン                              リポジトリー                            サイズ
======================================================================================================================================================
アップグレード:
 gitlab-ce                        x86_64                        17.4.2-ce.0.el9                         gitlab_gitlab-ce                        1.0 G

トランザクションの概要
======================================================================================================================================================
アップグレード  1 パッケージ

ダウンロードサイズの合計: 1.0 G
これでよろしいですか? [y/N]: y
パッケージのダウンロード:
gitlab-ce-17.4.2-ce.0.el9.x86_64.rpm                                                                                  3.2 MB/s | 1.0 GB     05:20
------------------------------------------------------------------------------------------------------------------------------------------------------
合計                                                                                                                  3.2 MB/s | 1.0 GB     05:20
トランザクションの確認を実行中
トランザクションの確認に成功しました。
トランザクションのテストを実行中
トランザクションのテストに成功しました。
トランザクションを実行中
  準備             :                                                                                                                              1/1
  scriptletの実行中: gitlab-ce-17.4.2-ce.0.el9.x86_64                                                                                             1/2
gitlab preinstall: It seems you are upgrading from 17.2 to 17.4.
gitlab preinstall: It is required to upgrade to the latest 17.3.x version first before proceeding.
gitlab preinstall: Please follow the upgrade documentation at https://docs.gitlab.com/ee/update/index.html#upgrade-paths
エラー: %prein(gitlab-ce-17.4.2-ce.0.el9.x86_64) スクリプトの実行に失敗しました。終了ステータス 1

Error in PREIN scriptlet in rpm package gitlab-ce
  検証             : gitlab-ce-17.4.2-ce.0.el9.x86_64                                                                                             1/2
  検証             : gitlab-ce-17.2.2-ce.0.el9.x86_64                                                                                             2/2
インストール済みの製品が更新されています。

失敗しました:
  gitlab-ce-17.2.2-ce.0.el9.x86_64                                          gitlab-ce-17.4.2-ce.0.el9.x86_64

エラー: トランザクションが失敗しました
```

[Upgrade Path](https://gitlab-com.gitlab.io/support/toolbox/upgrade-path/)を確認してから必要なバージョンを指定してバージョンアップする。

```bash
dnf install gitlab-ce-<version>
```
