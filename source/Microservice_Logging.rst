ログ出力を試す
####################


.. image:: ./_static/Microservice_Logging/architecture.drawio.svg


ログサーバ用コンテナの準備
==========================
まず、ローカル検証環境で準備する。

ローカル検証環境で、fluent.confを作成して、fluentdの設定ファイルを作成する。

.. code-block::

    <source>
    @type http
    port 9880
    bind 0.0.0.0
    </source>

    <match **>
    @type stdout
    </match>

fluentdの最新コンテナイメージを利用して、コンテナを起動する。

.. code-block::

    # コンテナ起動
    podman run -d --name fluentd -p 9880:9880 -v .:/fluentd/etc -e FLUENTD_CONF=fluent.conf fluent/fluentd:edge

    # テストログ送信
    curl -X POST -d 'json={"action":"test","user":"example"}' http://localhost:9880/sample.log

    # ログ確認
    [noim@rhel9 test_fluentd]$ podman logs fluentd
    2024-02-18 15:30:12 +0000 [info]: init supervisor logger path=nil rotate_age=nil rotate_size=nil
    2024-02-18 15:30:12 +0000 [info]: parsing config file is succeeded path="/fluentd/etc/fluent.conf"
    2024-02-18 15:30:12 +0000 [info]: gem 'fluentd' version '1.16.3'
    2024-02-18 15:30:12 +0000 [warn]: define <match fluent.**> to capture fluentd logs in top level is deprecated. Use <label @FLUENT_LOG> instead
    2024-02-18 15:30:12 +0000 [info]: using configuration file: <ROOT>
    <source>
        @type http
        port 9880
        bind "0.0.0.0"
    </source>
    <match **>
        @type stdout
    </match>
    </ROOT>
    2024-02-18 15:30:12 +0000 [info]: starting fluentd-1.16.3 pid=2 ruby="3.2.2"
    2024-02-18 15:30:12 +0000 [info]: spawn command to main:  cmdline=["/usr/bin/ruby", "-Eascii-8bit:ascii-8bit", "/usr/bin/fluentd", "--config", "/fluentd/etc/fluent.conf", "--plugin", "/fluentd/plugins", "--under-supervisor"]
    2024-02-18 15:30:13 +0000 [info]: #0 init worker0 logger path=nil rotate_age=nil rotate_size=nil
    2024-02-18 15:30:13 +0000 [info]: adding match pattern="**" type="stdout"
    2024-02-18 15:30:13 +0000 [info]: adding source type="http"
    2024-02-18 15:30:13 +0000 [warn]: #0 define <match fluent.**> to capture fluentd logs in top level is deprecated. Use <label @FLUENT_LOG> instead
    2024-02-18 15:30:13 +0000 [info]: #0 starting fluentd worker pid=11 ppid=2 worker=0
    2024-02-18 15:30:13 +0000 [info]: #0 fluentd worker is now running worker=0
    2024-02-18 15:30:13.192837127 +0000 fluent.info: {"pid":11,"ppid":2,"worker":0,"message":"starting fluentd worker pid=11 ppid=2 worker=0"}
    2024-02-18 15:30:13.193745831 +0000 fluent.info: {"worker":0,"message":"fluentd worker is now running worker=0"}
    2024-02-18 15:31:03.719726481 +0000 sample.log: {"action":"test","user":"example"}

