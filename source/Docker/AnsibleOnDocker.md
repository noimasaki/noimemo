# Ansibleコンテナを作る

Ansible実行環境をコンテナで準備できるようにする。

https://qiita.com/atlas-sword/items/2cd02beb120de22a3a9e

https://tk-ch.hatenablog.com/entry/20221010/1665411979


https://logmi.jp/tech/articles/329608


https://qiita.com/Shoma0210/items/7d7d24d7c3f95f19b427




## ベースイメージ
`quay.io/centos/centos:stream9`

## ansible-coreバージョン
[Ansible公式ドキュメント](https://docs.ansible.com/ansible/latest/)を参照して


## centos9コンテナをpullして手で構築してみる。
Dockerfile
```
# ベースイメージ
FROM quay.io/centos/centos:stream9

# システムアップデート
RUN dnf -y update && dnf clean all

# EPEL有効化
RUN dnf install -y epel-release

# Ansibleインストール
RUN dnf install -y ansible

# タイムゾーンをJSTに設定
RUN echo 'ZONE="Asia/Tokyo"' > /etc/sysconfig/clock
RUN rm -f /etc/localtime
RUN ln -fs /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

# コンテナの実行ユーザーをrootに設定
USER root

# コンテナを実行する際のコマンド (bashシェルを実行)
CMD ["/bin/bash"]
```

```
# コンテナビルド
docker build -t ansible-container .

# 起動
docker run --rm -it -v ./work:/mnt/data ansible-container
```


```
noimasaki@noi-MacBook ansible-training % docker pull quay.io/centos/centos:stream9
stream9: Pulling from centos/centos
0d9665cbb1e4: Pull complete 
Digest: sha256:8edcfab3ba262a926f3f911d5743bd894dce857fc80f74b615b68da3d05f4bde
Status: Downloaded newer image for quay.io/centos/centos:stream9
quay.io/centos/centos:stream9

What's Next?
  1. Sign in to your Docker account → docker login
  2. View a summary of image vulnerabilities and recommendations → docker scout quickview quay.io/centos/centos:stream9
noimasaki@noi-MacBook ansible-training % docker images
REPOSITORY              TAG       IMAGE ID       CREATED       SIZE
quay.io/centos/centos   stream9   e0618e7a2b75   5 days ago    158MB
postgres                latest    cff6b68a194a   7 weeks ago   432MB
noimasaki@noi-MacBook ansible-training % docker run -it e06 /bin/bash 
[root@8cc950fbeac2 /]# dnf update -y
CentOS Stream 9 - BaseOS                                                                                                          424 kB/s | 8.1 MB     00:19    
CentOS Stream 9 - AppStream                                                                                                       661 kB/s |  20 MB     00:30    
CentOS Stream 9 - Extras packages                                                                                                  36 kB/s |  17 kB     00:00    
Last metadata expiration check: 0:00:01 ago on Sun Jun 30 02:39:59 2024.
Dependencies resolved.
Nothing to do.
Complete!
[root@8cc950fbeac2 /]# dnf install -y epel-release
dnf install -y ansible
Last metadata expiration check: 0:00:25 ago on Sun Jun 30 02:39:59 2024.
Dependencies resolved.
==================================================================================================================================================================
 Package                                         Architecture                  Version                                 Repository                            Size
==================================================================================================================================================================
Installing:
 epel-release                                    noarch                        9-7.el9                                 extras-common                         19 k
Installing dependencies:
 dbus-libs                                       x86_64                        1:1.12.20-8.el9                         baseos                               152 k
 python3-dateutil                                noarch                        1:2.8.1-7.el9                           baseos                               288 k
 python3-dbus                                    x86_64                        1.2.18-2.el9                            baseos                               144 k
 python3-dnf-plugins-core                        noarch                        4.3.0-16.el9                            baseos                               264 k
 python3-six                                     noarch                        1.15.0-9.el9                            baseos                                37 k
 python3-systemd                                 x86_64                        234-18.el9                              baseos                                90 k
 systemd-libs                                    x86_64                        252-37.el9                              baseos                               680 k
Installing weak dependencies:
 dnf-plugins-core                                noarch                        4.3.0-16.el9                            baseos                                37 k
 epel-next-release                               noarch                        9-7.el9                                 extras-common                        8.1 k

Transaction Summary
==================================================================================================================================================================
Install  10 Packages

Total download size: 1.7 M
Installed size: 4.7 M
Downloading Packages:
(1/10): dnf-plugins-core-4.3.0-16.el9.noarch.rpm                                                                                  401 kB/s |  37 kB     00:00    
(2/10): python3-dateutil-2.8.1-7.el9.noarch.rpm                                                                                   1.5 MB/s | 288 kB     00:00    
(3/10): dbus-libs-1.12.20-8.el9.x86_64.rpm                                                                                        801 kB/s | 152 kB     00:00    
(4/10): python3-dbus-1.2.18-2.el9.x86_64.rpm                                                                                      1.4 MB/s | 144 kB     00:00    
(5/10): python3-six-1.15.0-9.el9.noarch.rpm                                                                                       627 kB/s |  37 kB     00:00    
(6/10): python3-systemd-234-18.el9.x86_64.rpm                                                                                     1.3 MB/s |  90 kB     00:00    
(7/10): python3-dnf-plugins-core-4.3.0-16.el9.noarch.rpm                                                                          2.7 MB/s | 264 kB     00:00    
(8/10): epel-next-release-9-7.el9.noarch.rpm                                                                                      116 kB/s | 8.1 kB     00:00    
(9/10): epel-release-9-7.el9.noarch.rpm                                                                                           265 kB/s |  19 kB     00:00    
(10/10): systemd-libs-252-37.el9.x86_64.rpm                                                                                       2.2 MB/s | 680 kB     00:00    
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                                             1.3 MB/s | 1.7 MB     00:01     
CentOS Stream 9 - BaseOS                                                                                                          1.6 MB/s | 1.6 kB     00:00    
Importing GPG key 0x8483C65D:
 Userid     : "CentOS (CentOS Official Signing Key) <security@centos.org>"
 Fingerprint: 99DB 70FA E1D7 CE22 7FB6 4882 05B5 55B3 8483 C65D
 From       : /etc/pki/rpm-gpg/RPM-GPG-KEY-centosofficial
Key imported successfully
CentOS Stream 9 - Extras packages                                                                                                 2.1 MB/s | 2.1 kB     00:00    
Importing GPG key 0x1D997668:
 Userid     : "CentOS Extras SIG (https://wiki.centos.org/SpecialInterestGroup) <security@centos.org>"
 Fingerprint: 363F C097 2F64 B699 AED3 968E 1FF6 A217 1D99 7668
 From       : /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-SIG-Extras-SHA512
Key imported successfully
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                                                                                          1/1 
  Installing       : systemd-libs-252-37.el9.x86_64                                                                                                          1/10 
  Running scriptlet: systemd-libs-252-37.el9.x86_64                                                                                                          1/10 
  Installing       : dbus-libs-1:1.12.20-8.el9.x86_64                                                                                                        2/10 
  Installing       : python3-dbus-1.2.18-2.el9.x86_64                                                                                                        3/10 
  Installing       : python3-systemd-234-18.el9.x86_64                                                                                                       4/10 
  Installing       : python3-six-1.15.0-9.el9.noarch                                                                                                         5/10 
  Installing       : python3-dateutil-1:2.8.1-7.el9.noarch                                                                                                   6/10 
  Installing       : python3-dnf-plugins-core-4.3.0-16.el9.noarch                                                                                            7/10 
  Installing       : dnf-plugins-core-4.3.0-16.el9.noarch                                                                                                    8/10 
  Installing       : epel-next-release-9-7.el9.noarch                                                                                                        9/10 
  Installing       : epel-release-9-7.el9.noarch                                                                                                            10/10 
  Running scriptlet: epel-release-9-7.el9.noarch                                                                                                            10/10 
Many EPEL packages require the CodeReady Builder (CRB) repository.
It is recommended that you run /usr/bin/crb enable to enable the CRB repository.

  Verifying        : dbus-libs-1:1.12.20-8.el9.x86_64                                                                                                        1/10 
  Verifying        : dnf-plugins-core-4.3.0-16.el9.noarch                                                                                                    2/10 
  Verifying        : python3-dateutil-1:2.8.1-7.el9.noarch                                                                                                   3/10 
  Verifying        : python3-dbus-1.2.18-2.el9.x86_64                                                                                                        4/10 
  Verifying        : python3-dnf-plugins-core-4.3.0-16.el9.noarch                                                                                            5/10 
  Verifying        : python3-six-1.15.0-9.el9.noarch                                                                                                         6/10 
  Verifying        : python3-systemd-234-18.el9.x86_64                                                                                                       7/10 
  Verifying        : systemd-libs-252-37.el9.x86_64                                                                                                          8/10 
  Verifying        : epel-next-release-9-7.el9.noarch                                                                                                        9/10 
  Verifying        : epel-release-9-7.el9.noarch                                                                                                            10/10 

Installed:
  dbus-libs-1:1.12.20-8.el9.x86_64        dnf-plugins-core-4.3.0-16.el9.noarch   epel-next-release-9-7.el9.noarch               epel-release-9-7.el9.noarch      
  python3-dateutil-1:2.8.1-7.el9.noarch   python3-dbus-1.2.18-2.el9.x86_64       python3-dnf-plugins-core-4.3.0-16.el9.noarch   python3-six-1.15.0-9.el9.noarch  
  python3-systemd-234-18.el9.x86_64       systemd-libs-252-37.el9.x86_64        

Complete!
Extra Packages for Enterprise Linux 9 - x86_64                                                                                    3.0 MB/s |  21 MB     00:07    
Extra Packages for Enterprise Linux 9 openh264 (From Cisco) - x86_64                                                              2.5 kB/s | 2.5 kB     00:00    
Extra Packages for Enterprise Linux 9 - Next - x86_64                                                                             531 kB/s | 274 kB     00:00    
Dependencies resolved.
==================================================================================================================================================================
 Package                                     Architecture                  Version                                         Repository                        Size
==================================================================================================================================================================
Installing:
 ansible                                     noarch                        1:7.7.0-1.el9                                   epel                              34 M
Installing dependencies:
 ansible-core                                x86_64                        1:2.14.17-1.el9                                 appstream                        2.6 M
 cracklib                                    x86_64                        2.9.6-27.el9                                    baseos                            94 k
 cracklib-dicts                              x86_64                        2.9.6-27.el9                                    baseos                           3.6 M
 git-core                                    x86_64                        2.43.0-1.el9                                    appstream                        4.4 M
 less                                        x86_64                        590-3.el9                                       baseos                           162 k
 libcbor                                     x86_64                        0.7.0-5.el9                                     baseos                            57 k
 libdb                                       x86_64                        5.3.28-54.el9                                   baseos                           735 k
 libeconf                                    x86_64                        0.4.1-4.el9                                     baseos                            27 k
 libedit                                     x86_64                        3.1-38.20210216cvs.el9                          baseos                           104 k
 libfdisk                                    x86_64                        2.37.4-18.el9                                   baseos                           155 k
 libfido2                                    x86_64                        1.13.0-2.el9                                    baseos                            99 k
 libpwquality                                x86_64                        1.4.4-8.el9                                     baseos                           119 k
 libutempter                                 x86_64                        1.2.1-6.el9                                     baseos                            27 k
 openssh                                     x86_64                        8.7p1-41.el9                                    baseos                           462 k
 openssh-clients                             x86_64                        8.7p1-41.el9                                    baseos                           718 k
 openssl                                     x86_64                        1:3.2.2-2.el9                                   baseos                           1.4 M
 pam                                         x86_64                        1.5.1-20.el9                                    baseos                           628 k
 python3-cffi                                x86_64                        1.14.5-5.el9                                    baseos                           253 k
 python3-cryptography                        x86_64                        36.0.1-4.el9                                    baseos                           1.2 M
 python3-packaging                           noarch                        20.9-5.el9                                      appstream                         77 k
 python3-ply                                 noarch                        3.11-14.el9                                     baseos                           106 k
 python3-pycparser                           noarch                        2.20-6.el9                                      baseos                           135 k
 python3-pyparsing                           noarch                        2.4.7-9.el9                                     baseos                           150 k
 python3-pyyaml                              x86_64                        5.4.1-6.el9                                     baseos                           205 k
 python3-resolvelib                          noarch                        0.5.4-5.el9                                     appstream                         34 k
 python3-setuptools                          noarch                        53.0.0-12.el9                                   baseos                           944 k
 sshpass                                     x86_64                        1.09-4.el9                                      appstream                         28 k
 util-linux                                  x86_64                        2.37.4-18.el9                                   baseos                           2.3 M
 util-linux-core                             x86_64                        2.37.4-18.el9                                   baseos                           465 k

Transaction Summary
==================================================================================================================================================================
Install  30 Packages

Total download size: 55 M
Installed size: 441 M
Downloading Packages:
(1/30): cracklib-2.9.6-27.el9.x86_64.rpm                                                                                          669 kB/s |  94 kB     00:00    
(2/30): less-590-3.el9.x86_64.rpm                                                                                                 880 kB/s | 162 kB     00:00    
(3/30): libcbor-0.7.0-5.el9.x86_64.rpm                                                                                            1.0 MB/s |  57 kB     00:00    
(4/30): libeconf-0.4.1-4.el9.x86_64.rpm                                                                                           1.0 MB/s |  27 kB     00:00    
(5/30): libedit-3.1-38.20210216cvs.el9.x86_64.rpm                                                                                 1.4 MB/s | 104 kB     00:00    
(6/30): libdb-5.3.28-54.el9.x86_64.rpm                                                                                            1.7 MB/s | 735 kB     00:00    
(7/30): libfdisk-2.37.4-18.el9.x86_64.rpm                                                                                         428 kB/s | 155 kB     00:00    
(8/30): libfido2-1.13.0-2.el9.x86_64.rpm                                                                                          1.3 MB/s |  99 kB     00:00    
(9/30): libutempter-1.2.1-6.el9.x86_64.rpm                                                                                        963 kB/s |  27 kB     00:00    
(10/30): libpwquality-1.4.4-8.el9.x86_64.rpm                                                                                      1.3 MB/s | 119 kB     00:00    
(11/30): openssh-8.7p1-41.el9.x86_64.rpm                                                                                          1.2 MB/s | 462 kB     00:00    
(12/30): openssh-clients-8.7p1-41.el9.x86_64.rpm                                                                                  1.4 MB/s | 718 kB     00:00    
(13/30): pam-1.5.1-20.el9.x86_64.rpm                                                                                              1.5 MB/s | 628 kB     00:00    
(14/30): python3-cffi-1.14.5-5.el9.x86_64.rpm                                                                                     1.5 MB/s | 253 kB     00:00    
(15/30): cracklib-dicts-2.9.6-27.el9.x86_64.rpm                                                                                   1.9 MB/s | 3.6 MB     00:01    
(16/30): python3-ply-3.11-14.el9.noarch.rpm                                                                                       2.1 MB/s | 106 kB     00:00    
(17/30): openssl-3.2.2-2.el9.x86_64.rpm                                                                                           1.5 MB/s | 1.4 MB     00:00    
(18/30): python3-pycparser-2.20-6.el9.noarch.rpm                                                                                  2.5 MB/s | 135 kB     00:00    
(19/30): python3-pyparsing-2.4.7-9.el9.noarch.rpm                                                                                 1.3 MB/s | 150 kB     00:00    
(20/30): python3-pyyaml-5.4.1-6.el9.x86_64.rpm                                                                                    2.5 MB/s | 205 kB     00:00    
(21/30): python3-setuptools-53.0.0-12.el9.noarch.rpm                                                                              3.1 MB/s | 944 kB     00:00    
(22/30): util-linux-core-2.37.4-18.el9.x86_64.rpm                                                                                 1.5 MB/s | 465 kB     00:00    
(23/30): python3-cryptography-36.0.1-4.el9.x86_64.rpm                                                                             1.3 MB/s | 1.2 MB     00:00    
(24/30): util-linux-2.37.4-18.el9.x86_64.rpm                                                                                      940 kB/s | 2.3 MB     00:02    
(25/30): python3-packaging-20.9-5.el9.noarch.rpm                                                                                  681 kB/s |  77 kB     00:00    
(26/30): python3-resolvelib-0.5.4-5.el9.noarch.rpm                                                                                666 kB/s |  34 kB     00:00    
(27/30): sshpass-1.09-4.el9.x86_64.rpm                                                                                            195 kB/s |  28 kB     00:00    
(28/30): ansible-core-2.14.17-1.el9.x86_64.rpm                                                                                    1.0 MB/s | 2.6 MB     00:02    
(29/30): git-core-2.43.0-1.el9.x86_64.rpm                                                                                         318 kB/s | 4.4 MB     00:14    
(30/30): ansible-7.7.0-1.el9.noarch.rpm                                                                                           1.9 MB/s |  34 MB     00:18    
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                                             2.3 MB/s |  55 MB     00:23     
Extra Packages for Enterprise Linux 9 - x86_64                                                                                    1.6 MB/s | 1.6 kB     00:00    
Importing GPG key 0x3228467C:
 Userid     : "Fedora (epel9) <epel@fedoraproject.org>"
 Fingerprint: FF8A D134 4597 106E CE81 3B91 8A38 72BF 3228 467C
 From       : /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-9
Key imported successfully
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                                                                                          1/1 
  Installing       : cracklib-2.9.6-27.el9.x86_64                                                                                                            1/30 
  Installing       : cracklib-dicts-2.9.6-27.el9.x86_64                                                                                                      2/30 
  Installing       : sshpass-1.09-4.el9.x86_64                                                                                                               3/30 
  Installing       : python3-resolvelib-0.5.4-5.el9.noarch                                                                                                   4/30 
  Installing       : util-linux-core-2.37.4-18.el9.x86_64                                                                                                    5/30 
  Running scriptlet: util-linux-core-2.37.4-18.el9.x86_64                                                                                                    5/30 
  Installing       : python3-setuptools-53.0.0-12.el9.noarch                                                                                                 6/30 
  Installing       : python3-pyyaml-5.4.1-6.el9.x86_64                                                                                                       7/30 
  Installing       : python3-pyparsing-2.4.7-9.el9.noarch                                                                                                    8/30 
  Installing       : python3-packaging-20.9-5.el9.noarch                                                                                                     9/30 
  Installing       : python3-ply-3.11-14.el9.noarch                                                                                                         10/30 
  Installing       : python3-pycparser-2.20-6.el9.noarch                                                                                                    11/30 
  Installing       : python3-cffi-1.14.5-5.el9.x86_64                                                                                                       12/30 
  Installing       : python3-cryptography-36.0.1-4.el9.x86_64                                                                                               13/30 
  Installing       : openssl-1:3.2.2-2.el9.x86_64                                                                                                           14/30 
  Running scriptlet: libutempter-1.2.1-6.el9.x86_64                                                                                                         15/30 
  Installing       : libutempter-1.2.1-6.el9.x86_64                                                                                                         15/30 
  Installing       : libfdisk-2.37.4-18.el9.x86_64                                                                                                          16/30 
  Installing       : libedit-3.1-38.20210216cvs.el9.x86_64                                                                                                  17/30 
  Installing       : libeconf-0.4.1-4.el9.x86_64                                                                                                            18/30 
  Installing       : libdb-5.3.28-54.el9.x86_64                                                                                                             19/30 
  Installing       : pam-1.5.1-20.el9.x86_64                                                                                                                20/30 
  Installing       : libpwquality-1.4.4-8.el9.x86_64                                                                                                        21/30 
  Installing       : util-linux-2.37.4-18.el9.x86_64                                                                                                        22/30 
warning: /etc/adjtime created as /etc/adjtime.rpmnew

  Running scriptlet: openssh-8.7p1-41.el9.x86_64                                                                                                            23/30 
  Installing       : openssh-8.7p1-41.el9.x86_64                                                                                                            23/30 
  Installing       : libcbor-0.7.0-5.el9.x86_64                                                                                                             24/30 
  Installing       : libfido2-1.13.0-2.el9.x86_64                                                                                                           25/30 
  Installing       : openssh-clients-8.7p1-41.el9.x86_64                                                                                                    26/30 
  Running scriptlet: openssh-clients-8.7p1-41.el9.x86_64                                                                                                    26/30 
  Installing       : less-590-3.el9.x86_64                                                                                                                  27/30 
  Installing       : git-core-2.43.0-1.el9.x86_64                                                                                                           28/30 
  Installing       : ansible-core-1:2.14.17-1.el9.x86_64                                                                                                    29/30 
  Installing       : ansible-1:7.7.0-1.el9.noarch                                                                                                           30/30 
  Running scriptlet: ansible-1:7.7.0-1.el9.noarch                                                                                                           30/30 
  Verifying        : cracklib-2.9.6-27.el9.x86_64                                                                                                            1/30 
  Verifying        : cracklib-dicts-2.9.6-27.el9.x86_64                                                                                                      2/30 
  Verifying        : less-590-3.el9.x86_64                                                                                                                   3/30 
  Verifying        : libcbor-0.7.0-5.el9.x86_64                                                                                                              4/30 
  Verifying        : libdb-5.3.28-54.el9.x86_64                                                                                                              5/30 
  Verifying        : libeconf-0.4.1-4.el9.x86_64                                                                                                             6/30 
  Verifying        : libedit-3.1-38.20210216cvs.el9.x86_64                                                                                                   7/30 
  Verifying        : libfdisk-2.37.4-18.el9.x86_64                                                                                                           8/30 
  Verifying        : libfido2-1.13.0-2.el9.x86_64                                                                                                            9/30 
  Verifying        : libpwquality-1.4.4-8.el9.x86_64                                                                                                        10/30 
  Verifying        : libutempter-1.2.1-6.el9.x86_64                                                                                                         11/30 
  Verifying        : openssh-8.7p1-41.el9.x86_64                                                                                                            12/30 
  Verifying        : openssh-clients-8.7p1-41.el9.x86_64                                                                                                    13/30 
  Verifying        : openssl-1:3.2.2-2.el9.x86_64                                                                                                           14/30 
  Verifying        : pam-1.5.1-20.el9.x86_64                                                                                                                15/30 
  Verifying        : python3-cffi-1.14.5-5.el9.x86_64                                                                                                       16/30 
  Verifying        : python3-cryptography-36.0.1-4.el9.x86_64                                                                                               17/30 
  Verifying        : python3-ply-3.11-14.el9.noarch                                                                                                         18/30 
  Verifying        : python3-pycparser-2.20-6.el9.noarch                                                                                                    19/30 
  Verifying        : python3-pyparsing-2.4.7-9.el9.noarch                                                                                                   20/30 
  Verifying        : python3-pyyaml-5.4.1-6.el9.x86_64                                                                                                      21/30 
  Verifying        : python3-setuptools-53.0.0-12.el9.noarch                                                                                                22/30 
  Verifying        : util-linux-2.37.4-18.el9.x86_64                                                                                                        23/30 
  Verifying        : util-linux-core-2.37.4-18.el9.x86_64                                                                                                   24/30 
  Verifying        : ansible-core-1:2.14.17-1.el9.x86_64                                                                                                    25/30 
  Verifying        : git-core-2.43.0-1.el9.x86_64                                                                                                           26/30 
  Verifying        : python3-packaging-20.9-5.el9.noarch                                                                                                    27/30 
  Verifying        : python3-resolvelib-0.5.4-5.el9.noarch                                                                                                  28/30 
  Verifying        : sshpass-1.09-4.el9.x86_64                                                                                                              29/30 
  Verifying        : ansible-1:7.7.0-1.el9.noarch                                                                                                           30/30 

Installed:
  ansible-1:7.7.0-1.el9.noarch         ansible-core-1:2.14.17-1.el9.x86_64    cracklib-2.9.6-27.el9.x86_64             cracklib-dicts-2.9.6-27.el9.x86_64       
  git-core-2.43.0-1.el9.x86_64         less-590-3.el9.x86_64                  libcbor-0.7.0-5.el9.x86_64               libdb-5.3.28-54.el9.x86_64               
  libeconf-0.4.1-4.el9.x86_64          libedit-3.1-38.20210216cvs.el9.x86_64  libfdisk-2.37.4-18.el9.x86_64            libfido2-1.13.0-2.el9.x86_64             
  libpwquality-1.4.4-8.el9.x86_64      libutempter-1.2.1-6.el9.x86_64         openssh-8.7p1-41.el9.x86_64              openssh-clients-8.7p1-41.el9.x86_64      
  openssl-1:3.2.2-2.el9.x86_64         pam-1.5.1-20.el9.x86_64                python3-cffi-1.14.5-5.el9.x86_64         python3-cryptography-36.0.1-4.el9.x86_64 
  python3-packaging-20.9-5.el9.noarch  python3-ply-3.11-14.el9.noarch         python3-pycparser-2.20-6.el9.noarch      python3-pyparsing-2.4.7-9.el9.noarch     
  python3-pyyaml-5.4.1-6.el9.x86_64    python3-resolvelib-0.5.4-5.el9.noarch  python3-setuptools-53.0.0-12.el9.noarch  sshpass-1.09-4.el9.x86_64                
  util-linux-2.37.4-18.el9.x86_64      util-linux-core-2.37.4-18.el9.x86_64  

Complete!
[root@8cc950fbeac2 /]# 
[root@8cc950fbeac2 /]# 
[root@8cc950fbeac2 /]# 
[root@8cc950fbeac2 /]# ansible --version
ansible [core 2.14.17]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3.9/site-packages/ansible
  ansible collection location = /root/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/bin/ansible
  python version = 3.9.19 (main, Jun 11 2024, 00:00:00) [GCC 11.4.1 20231218 (Red Hat 11.4.1-3)] (/usr/bin/python3)
  jinja version = 3.1.2
  libyaml = True

```