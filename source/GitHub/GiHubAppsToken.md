# GitHub Appsトークンの発行・実装方法
本記事では以下をまとめる。
 - GitHub Appsトークンとは
 - GitHub Appsの作成・インストール方法
 - GitHub ActionsでGitHub Appsトークンを利用する方法

## GitHub Appsトークンとは
GitHub Actionsでリポジトリにpushしたいなど、ワークフローの内容によっては権限が必要な作業がある。
用途ごとの権限をGitHubAppsトークンとして発行し、ワークフローに適用してあげれば、適切な権限管理が可能となる機能である。

同様な機能として、Personal Access Tokensなどがあるが、classic扱いとなっている為、GitHub Appsトークンを利用することが望ましい。

## GitHub appsのセットアップ
### 1. GitHub Appsを作成
Organizationsではなく、個人アカウントの場合はここにアクセス

[https://github.com/settings/apps/new](https://github.com/settings/apps/new)

- GitHub Apps name(*) : グローバルに一意の名前（例えば`ユーザ名ActionTokenGen`）
- Description : 任意のDescription
- Homepage URL(*) : 適当なダミー値でもOK（例えば`https://example.com`）

![name & URL](./GitHubAppsToken/setting1.png)

Webhookは不要なのでチェックを外す

![Webhook](./GitHubAppsToken/setting2.png)

Permissionsには権限を設定する。
今回はリポジトリ内のファイル（つまりContents）を書き換えたいので、次のように設定する。
- Repository permissions > Contents > Read and write

![Permissions](./GitHubAppsToken/setting3.png)

プライベート運用のため、「Only on this account」へチェックが入っていることを確認して「Greate GitHub App」をクリックすれば完了。

管理画面が表示される。
ここで確認できる「APP ID」は後程利用するのでメモする。

![General](./GitHubAppsToken/setting4.png)

### 2. 署名用秘密鍵の生成
トークンの払い出しに使用する、署名用秘密鍵を生成する。

![GenPrivateKey](./GitHubAppsToken/setting5.png)

自動で`<App名>.<作成日>.private-key`というファイルがローカルにダウンロードされる。
これを後にGitHubのSeacretsへ登録し、ローカルからも削除する。

### 3. GitHub Appsをアカウントへインストール
GitHub Appsは作成しただけでは使えず、アカウントにインストールする必要がある。「Install」をクリック。

![InstallGitHubApps](./GitHubAppsToken/setting6.png)

どのリポジトリにインストールするか聞かれるので、選択する。
- All repositories（全リポジトリを許可）: 運用は楽だがセキュリティ的にイマイチ
- Only select repositories（特定リポジトリのみ許可）: セキュアだが運用は少し煩雑

今回は「Only select repositories」選択した。

![ChooseRepo](./GitHubAppsToken/setting7.png)

### 4. SecretsにApp IDと秘密鍵を登録
App IDと秘密鍵をGitHub Actionsから参照できるよう、Secretsへ登録する。

対象リポジトリを開き、`Settings > Secrets and variables > Actions > New repository secret`を選択
次の２つのシークレットを登録する
- Name(*): PRIVATE_KEY
- Secret(*): ダウンロードした署名用秘密鍵 ※「-----BEGIN RSA PRIVATE KEY-----」から「-----END RSA PRIVATE KEY-----」まで

- Name(*): APP_ID
- Secret(*): GitHub Apps作成時に生成されたIDを記載

![RegiPrivateKey](./GitHubAppsToken/setting8.png)

## GitHub ActionsでGitHub Appsトークンを利用する方法
例として下記のように記載する。（動作確認していないので
```yaml
    # トークンを作成
    - name: Generate GitHub Apps token
      id: generate-token
      uses: tibdex/github-app-token@v1
      with:
        app_id: ${{ secrets.APP_ID }}
        private_key: ${{ secrets.PRIVATE_KEY }}
    
    - name: Commit and push html
      env:  # 
        GITHUB_TOKEN: ${{ steps.generate-token.outputs.token }}
      run: |
        git config user.name "GitHub Actions Bot"
        git add -A
        git commit -m "Converted MD files to HTML" || echo "No changes to commit"
        git push
```

## 参考
[https://zenn.dev/tmknom/articles/github-apps-token](https://zenn.dev/tmknom/articles/github-apps-token)