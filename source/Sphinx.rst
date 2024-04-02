##################################
Sphinx導入
##################################

`Sphinx <https://www.sphinx-doc.org/ja/master/>`_ をHTMLビルダーとして利用し、ドキュメンテーションする。

既にPythonがインストールされていることを前提とする。


1. Sphinxインストール
========================
1. コマンドプロンプトを起動して、Pythonがインストールされていることを確認する

.. code-block::

    C:\Users\masak>python --version
    Python 3.11.4

2. pipコマンドでSphinxインストール

.. code-block::

    C:\Users\masak>pip install -U sphinx

3. インストールされたことを確認

.. code-block::

    C:\Users\masak>sphinx-build --version
    sphinx-build 7.2.6


2. プロジェクト作成
========================
1. プロジェクトを作成したい任意のディレクトリで、プロジェクトを作成

.. code-block::

    C:\Users\masak\ドキュメント\noimemo>sphinx-quickstart
    Welcome to the Sphinx 7.2.6 quickstart utility.

    Please enter values for the following settings (just press Enter to
    accept a default value, if one is given in brackets).

    Selected root path: .

    You have two options for placing the build directory for Sphinx output.
    Either, you use a directory "_build" within the root path, or you separate
    "source" and "build" directories within the root path.
    > Separate source and build directories (y/n) [n]: y

    The project name will occur in several places in the built documentation.
    > Project name: noimemo
    > Author name(s): noim
    > Project release []:

    If the documents are to be written in a language other than English,
    you can select a language here by its language code. Sphinx will then
    translate text that it generates into that language.

    For a list of supported codes, see
    https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-language.
    > Project language [en]: ja

    Creating file C:\Users\masak\ドキュメント\noimemo\source\conf.py.
    Creating file C:\Users\masak\ドキュメント\noimemo\source\index.rst.
    Creating file C:\Users\masak\ドキュメント\noimemo\Makefile.
    Creating file C:\Users\masak\ドキュメント\noimemo\make.bat.

    Finished: An initial directory structure has been created.

    You should now populate your master file C:\Users\masak\ドキュメント\noimemo\source\index.rst and create other documentation
    source files. Use the Makefile to build the docs, like so:
    make builder
    where "builder" is one of the supported builders, e.g. html, latex or linkcheck.


2. Sphinxの拡張テーマ（sphinx_rtd_theme）をインストール



1. 記事作成・ビルド
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


5. [拡張機能] コピーボタン
============================
コードブロックにコピーボタンを追加する。

#. sphinx-copybutton インストール

    pip install sphinx-copybutton

#. conf.pyに追記

    extensions = [
        ...,
        'sphinx_copybutton',
    ]

コードブロックをそのままビルドすれば、コピーボタンが追加されている。