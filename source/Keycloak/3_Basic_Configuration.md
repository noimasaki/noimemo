## 基本設定

Keycloak の基本設定には、Realm の作成、クライアント設定、ユーザー管理、ロールやグループの設定があります。以下では、それぞれの登場人物と関係性を図式化しながら説明します。

### 1. Realm の作成と管理

Realm は、Keycloak の中でユーザーやクライアントをまとめて管理するための単位です。システム全体を分割して管理したい場合、異なるプロジェクトや環境ごとに Realm を作成します。

```
[Realm A] - [ユーザー、クライアント、ロール、グループ]
[Realm B] - [ユーザー、クライアント、ロール、グループ]
```

- Realm A と Realm B は、互いに独立した空間です。各 Realm 内で設定やユーザーは隔離されています。

### 2. クライアント設定

クライアントは、Keycloak に認証を依頼する外部のアプリケーションやサービスです。クライアント設定を行うことで、特定のアプリケーションに対する認証や認可を管理できます。

```
[Realm]
  └── [クライアント1] - [OpenID Connectの設定]
  └── [クライアント2] - [SAMLの設定]
```

- クライアント 1、クライアント 2 は、それぞれ異なるプロトコル（OpenID Connect や SAML）を使用して認証を行います。

### 3. ユーザーの作成と管理

ユーザーは、Keycloak を通じて認証される個々の利用者です。ユーザーごとに、認証情報（ID とパスワード）や属性（氏名、メールアドレスなど）を管理します。

```
[Realm]
  └── [ユーザー1] - [属性、認証情報]
  └── [ユーザー2] - [属性、認証情報]
```

- ユーザー 1 とユーザー 2 は、それぞれ個別に管理され、異なる属性や認証情報を持ちます。

### 4. ロールとグループの設定

ロールは、ユーザーに対するアクセス権限を表すもので、グループは複数のユーザーをまとめたものです。ユーザーにロールを割り当てることで、アクセスできるリソースを制御します。

```
[グループA]
  ├── [ユーザー1]
  ├── [ユーザー2]

[ロールX] - [特定のアクセス権限]
  └── [ユーザー1]
```

- グループ A には複数のユーザーが所属し、まとめて管理が可能です。
- ロール X は特定のアクセス権限を表し、ユーザー 1 に割り当てられています。
