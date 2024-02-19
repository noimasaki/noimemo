###############################
RHEL9サーバ構築
###############################

実現したいこと

- GitLabサーバ
- 外部からのアクセス（SSH）
- 外部からのアクセス（RDP）

GitLabサーバ
===============
`公式サイト <https://about.gitlab.com/ja-jp/install/#almalinux>`_ を参考にインストールする。

#. firewallルールを確認し、許可されていない場合は`http`と`https`を許可する

    [root@rhel9 srv]# firewall-cmd --list-all
        public (active)
        target: default
        icmp-block-inversion: no
        interfaces: wlo1
        sources: 
        services: cockpit dhcpv6-client ssh
        ports: 
        protocols: 
        forward: yes
        masquerade: no
        forward-ports: 
        source-ports: 
        icmp-blocks: 
        rich rules:
    [root@rhel9 srv]# firewall-cmd --permanent --add-service=http
    success
    [root@rhel9 srv]# firewall-cmd --permanent --add-service=https
    success
    [root@rhel9 srv]# systemctl reload firewalld

#. パッケージインストール

    curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.rpm.sh | sudo bash
    sudo EXTERNAL_URL="https://gitlab.example.com" dnf install -y gitlab-ee




