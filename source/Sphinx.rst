##################################
Sphinx導入
##################################

`Sphinx <https://www.sphinx-doc.org/ja/master/>`_ をHTMLビルダーとして利用し、ドキュメンテーションする。


1. Sphinxインストール
========================


2. プロジェクト作成
========================

3. 記事作成・ビルド
========================

4. [拡張機能] Mermaid
========================
ガントチャートやシーケンス図を簡単に生成できるツール。
`pip install <https://github.com/mgaitan/sphinxcontrib-mermaid?tab=readme-ov-file#installation>`_ して、拡張機能を有効化するだけ。

#. Mermaidインストール

    pip install sphinxcontrib-mermaid

#. conf.pyに追記

    extensions = [
        ...,
        'sphinxcontrib.mermaid'
    ]

