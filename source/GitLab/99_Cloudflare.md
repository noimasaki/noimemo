# Cloudflare 経由で GitLab を利用する

Gitlab では http でリッスンし、Cloudflare にて https でリッスンする時には`external_url`の設定まわりとリバースプロキシが存在する場合に発生するエラーが出やすい。

- `/etc/gitlab/gitlab.rb`の設定のポイント
- `external_url`はユーザが利用する URL と一致させるため、`https`にすると良い
- ただ、そうすると nginx が 443 ポートでリッスンしようとするため、以下の設定をする

```bash
nginx['listen_port'] = 80
nginx['listen_https'] = false
```

これで、gitlab としては実際には http でリッスンするが、リダイレクトなどの内部処理には https にしてくれる。（実際には cloudflare 側で http から https にリダイレクトしてくれるので実運用は問題ないが、gitlab からユーザに URL 含むメール等で http で表示するとダサいので、この設定にした。）
