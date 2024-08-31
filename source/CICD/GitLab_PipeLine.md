# GitLabパイプライン
`.gitlab-ci.yml`の書き方をメモ

## 1. 基本 (shell execution)
GitLabリポジトリのトップディレクトリに`.gitlab-ci.yml`を作成して記述する

```bash
# 各stageの実行順序を記載
#  -> stageはjob(=タスク)をグループ化したもの
#  -> build→deployの順に実施
stages:
  - build
  - deploy

# job名
build-job:
  stage: build      # このjobをbuildステージに設定
  script:           # 実際のjobで実行するスクリプト
    - echo "Compiling the code"
    - mkdir ./build
    - echo "This is Build File!!" >> ./build/output.txt
  artifacts:        # 生成されたファイルはstage間で共有されない -> artifactsで指定されたファイルは共有できる
    paths:
      - "build/"    # buildディレクトリ配下のファイルをartifactsとして指定

# job名
deploy-job:
  stage: deploy  # このjobをdeployステージに設定
  script:
    - mv build/ public/
  artifacts:
    paths:
      - "public/"


```

## 2. dockerエグゼキューション



## 参考
- [CI/CDを使ったアプリケーションの構築](https://gitlab-docs.creationline.com/ee/topics/build_your_application.html)
- [podman](https://gitlab-docs.creationline.com/runner/executors/docker.html#podman%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6docker%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%82%92%E5%AE%9F%E8%A1%8C%E3%81%97%E3%81%BE%E3%81%99)