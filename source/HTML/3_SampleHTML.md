# HTML のサンプル

```html
<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>シンプルなHTMLページ</title>
  </head>
  <body>
    <header>
      <h1>私のウェブページ</h1>
      <nav>
        <a href="#about">私について</a> |
        <a href="#contact">お問い合わせ</a>
      </nav>
    </header>

    <section id="about">
      <h2>私について</h2>
      <p>
        こんにちは！私はウェブ開発の学習を始めたばかりです。このページでは、HTMLの基本について紹介します。
      </p>
    </section>

    <section id="contact">
      <h2>お問い合わせ</h2>
      <form action="/submit" method="post">
        <label for="name">名前:</label>
        <input type="text" id="name" name="name" required /><br /><br />

        <label for="email">メールアドレス:</label>
        <input type="email" id="email" name="email" required /><br /><br />

        <button type="submit">送信</button>
      </form>
    </section>

    <footer>
      <p>&copy; 2024 私のウェブページ</p>
    </footer>
  </body>
</html>
```

## ボタン選択・本日の日付

```html
<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>収入記録</title>
    <style>
      body {
        font-family: "Arial", sans-serif;
      }

      .container {
        width: 90%;
        margin: 0 auto;
      }

      .input-group {
        margin-bottom: 1rem;
      }

      .button-group button {
        margin: 0.5rem;
        padding: 10px 15px;
        border: none;
        border-radius: 8px;
        background-color: #e0e0e0;
      }

      .button-group button.selected {
        background-color: #a5d6a7;
        /* 選択されたボタンの色 */
      }

      .submit-button {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        padding: 15px;
        background-color: #66bb6a;
        color: white;
        font-size: 1.2rem;
        border: none;
      }
    </style>
  </head>

  <body>
    <div class="container">
      <h2>収入記録</h2>
      <form action="/income_record" method="post">
        <!-- 金額入力 -->
        <div class="input-group">
          <label for="amount">金額 (JPY):</label>
          <input type="number" id="amount" name="amount" min="0" required />
        </div>

        <!-- 日付入力 -->
        <div class="input-group">
          <label for="date">日付:</label>
          <input type="date" id="date" name="date" required />
        </div>

        <!-- メモ入力 -->
        <div class="input-group">
          <label for="memo">メモ:</label>
          <input type="text" id="memo" name="memo" />
        </div>

        <!-- カテゴリー選択 -->
        <div class="input-group button-group">
          <button
            type="button"
            class="selected"
            onclick="setCategory('臨時収入')"
          >
            臨時収入
          </button>
          <button type="button" onclick="setCategory('補助金（会社）')">
            補助金（会社）
          </button>
          <button type="button" onclick="setCategory('補助金（公的）')">
            補助金（公的）
          </button>
          <button type="button" onclick="setCategory('その他')">その他</button>
        </div>

        <input type="hidden" id="category" name="category" value="臨時収入" />

        <!-- 記録ボタン -->
        <div class="input-group">
          <button type="submit" class="submit-button">記録する</button>
        </div>
      </form>
    </div>

    <script>
      // ページがロードされた時に本日の日付を設定する関数
      window.onload = function () {
        // 今日の日付
        let today = new Date();
        // フォーマットを"YYYY-MM-DD"形式にする
        let year = today.getFullYear();
        let month = ("0" + (today.getMonth() + 1)).slice(-2); // 月を2桁にする
        let day = ("0" + today.getDate()).slice(-2); // 日を2桁にする

        // 日付フィールドに本日の日付を設定
        document.getElementById("date").value = year + "-" + month + "-" + day;
      };

      // 選択されたカテゴリーボタンの色を変える関数
      function setCategory(value) {
        // 隠しフィールドに対応するカテゴリの値を設定
        document.getElementById("category").value = value;
        let buttons = document.querySelectorAll(".button-group button");
        // '.button-group button'の全てのボタンから"selected"クラスを削除
        buttons.forEach(function (button) {
          button.classList.remove("selected");
        });
        // クリックされたボタンに "selected" クラスを追加
        event.target.classList.add("selected");
      }
    </script>
  </body>
</html>
```
