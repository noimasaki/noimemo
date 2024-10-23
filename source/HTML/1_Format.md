# HTML 文章の構成

## パターン 1: シンプルな HTML

vscode であれば、ショートカットで入力できる

1. html ファイルを作成
2. ファイルに`!`を入力
3. `Tab`キーを押す

```html
<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>シンプルなHTML</title>
  </head>
  <body>
    <h1>見出し</h1>
    <p>これは段落です。</p>
  </body>
</html>
```

## パターン 2: CSS と JavaScript を利用

```html
<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>HTML文書の基本構成</title>
    <link rel="stylesheet" href="/css/styles.css" />
    <!-- スタイルシートを追加 -->
    <style>
      /* 簡単なスタイル設定 */
      body {
        font-family: "Arial", sans-serif;
      }
    </style>
  </head>
  <body>
    <h1>見出し</h1>
    <p>これは段落です。</p>
  </body>
</html>
```

## パターン 3: シンプルな Thymleaf

```html
<!DOCTYPE html>
<html lang="ja" xmlns:th="http://www.thymeleaf.org">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Thymeleaf文書の基本構成</title>
  </head>
  <body>
    <h1 th:text="${title}">デフォルトの見出し</h1>
    <p th:text="${message}">これは段落です。</p>
  </body>
</html>
```

## パターン 4: CSS と JavaScript を利用した Thymleaf
