# Sphinxによるドキュメント作成
SphinxとVisual Stadio Codeを使ったドキュメント作成環境を整える。

## Sphinxインストール
[公式ドキュメント](https://www.sphinx-doc.org/ja/master/usage/installation.html#)を参考にする。本手順ではすでにPythonがインストールされていることを前提とした手順。

1. コマンドプロンプト(Windows)もしくはターミナル(Mac)を起動して、Pythonがインストールされていることを確認する
```
C:\Users\masak>python --version
Python 3.11.4
```

2. pipコマンドでSphinxインストール
```
C:\Users\masak>pip install -U sphinx
```

3. インストールされたことを確認
```
C:\Users\masak>sphinx-build --version
sphinx-build 7.2.6
```


