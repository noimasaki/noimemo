# HTML 文章の構成

```html
<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>HTML文書の基本構成</title>
  </head>
  <body>
    <h1>見出し</h1>
    <p>これは段落です。</p>
  </body>
</html>
```

Thymleaf の場合はこんな感じ

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
