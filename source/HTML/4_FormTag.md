# フォームタグ

以下のサンプルについて説明します。

```html
<form action="/submit" method="post">
  <label for="name">名前:</label>
  <input type="text" id="name" name="name" required /><br /><br />

  <label for="email">メールアドレス:</label>
  <input type="email" id="email" name="email" required /><br /><br />

  <button type="submit">送信</button>
</form>
```

1. `<label for="name">`で、`input`タグに付与された`id="name"`属性に対してのラベルを付与している
2. HTML からサーバへは、`input`タグの`name`属性と値のセットが渡される

つまり、id 属性は HTML 内のみに利用され、HTML からサーバへ渡される値に対するキーは`name`属性で表現される。
