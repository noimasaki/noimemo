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
ガントチャートやシーケンス図を簡単に生成できる`ツール <https://github.com/mgaitan/sphinxcontrib-mermaid?tab=readme-ov-file#installation>`_

GUIで生成する`Mermaid Live <https://mermaid.live/>`_ も存在する。

#. Mermaidインストール

    pip install sphinxcontrib-mermaid

#. conf.pyに追記

    extensions = [
        ...,
        'sphinxcontrib.mermaid'
    ]

#. 記載例（ガントチャート）

.. code-block::

    .. mermaid::
    
        gantt
            title プロジェクトA
            dateFormat  YYYY-MM-DD
            excludes    weekends
            section  概要
                プロジェクト開始 : milestone, m1, 2023-02-01, 0d
                開発開始 : milestone, m2, after a1, 0d
                開発完了 : milestone, m3, after a4, 0d
                テスト完了 : milestone, m3, after b4, 0d
            section 開発
                開発準備 :done,a1, 2023-02-06, 2d
                開発（モジュールA） :done,a2, after a1, 2d
                開発（モジュールB） :active, a3, after a2, 3d
                開発（モジュールC） :a4, after a3, 5d
            section テスト
                テスト準備 :done, b1, 2023-02-10  , 2d
                テスト（モジュールA） :crit, active, b2, after a2 b1  , 2d
                テスト（モジュールB） :crit, b3, after a3 b2  , 2d
                テスト（モジュールC） :crit, b4, after a4 b3  , 2d


.. mermaid::

    gantt
        title プロジェクトA
        dateFormat  YYYY-MM-DD
        excludes    weekends
        section  概要
            プロジェクト開始 : milestone, m1, 2023-02-01, 0d
            開発開始 : milestone, m2, after a1, 0d
            開発完了 : milestone, m3, after a4, 0d
            テスト完了 : milestone, m3, after b4, 0d
        section 開発
            開発準備 :done,a1, 2023-02-06, 2d
            開発（モジュールA） :done,a2, after a1, 2d
            開発（モジュールB） :active, a3, after a2, 3d
            開発（モジュールC） :a4, after a3, 5d
        section テスト
            テスト準備 :done, b1, 2023-02-10  , 2d
            テスト（モジュールA） :crit, active, b2, after a2 b1  , 2d
            テスト（モジュールB） :crit, b3, after a3 b2  , 2d
            テスト（モジュールC） :crit, b4, after a4 b3  , 2d
