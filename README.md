# roto6_tutorial
# ロト6予想サービス(チュートリアル)

Python / Django で作る、ロト6の予想を表示するシンプルなWebアプリです。
AI開発の学習用チュートリアルとして作成した簡易版です。

## 機能

- トップページに予測を3パターン表示
  - 頻出パターン(過去の出現頻度が高い数字)
  - スランプ数字パターン(出現頻度が低い数字)
  - 重み付けランダム(出現頻度で重み付けした抽選)
- 管理画面(Django Admin)から抽選結果を登録すると、予測が自動更新
- 管理画面で分析ダッシュボードを閲覧可能(pandas/numpyによる集計 + Chart.jsでグラフ表示)
- Docker対応

## 技術スタック

- Python 3.11
- Django 4.2.4
- pandas / numpy(集計・分析)
- Chart.js(グラフ描画、CDN経由)
- Docker / docker-compose

## ディレクトリ構成

```
roto6_tutorial/
├── manage.py
├── config/                 # Djangoプロジェクト設定
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── predictor/
│   ├── data/
│   │   └── draws.json       # 過去の抽選結果データ
│   ├── logic.py              # 予測ロジック・draws.json読み書き
│   ├── analytics.py          # pandas/numpyによる集計処理
│   ├── forms.py               # 抽選結果登録フォーム
│   ├── admin.py                # admin拡張(登録・分析画面)
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       ├── predictor/
│       │   └── top.html         # トップページ
│       └── admin/
│           ├── add_draw.html      # 抽選結果登録フォーム
│           ├── add_draw_done.html # 登録完了画面
│           └── analytics.html     # 分析ダッシュボード
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── requirements.txt
```

## セットアップ(ローカル)

```bash
python3 -m venv venv
source venv/bin/activate   # Windowsの場合: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser

python manage.py runserver
```

`http://127.0.0.1:8000/` でトップページ、`http://127.0.0.1:8000/admin/` で管理画面にアクセスできます。

## セットアップ(Docker)

```bash
docker compose up --build
```

初回起動後、別ターミナルでDBのマイグレーションと管理ユーザー作成を行います。

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

## 使い方

1. `/admin/` にログイン
2. `/admin/predictor/add-draw/` から抽選結果を登録
3. トップページ(`/`)で予測が更新されていることを確認
4. `/admin/predictor/analytics/` で出現頻度などの分析を閲覧

## データについて

`predictor/data/draws.json` に過去の抽選結果を蓄積していきます。データ件数が増えるほど頻度分析やスランプ数字パターンの精度(という名の面白さ)が上がります。

## 注意事項

宝くじの当選番号は数学的にランダムであり、本サービスの予測は過去の傾向を可視化したものに過ぎず、当選を保証するものではありません。学習・娯楽目的でご利用ください。

## 今後の拡張案

- 直近N回だけに絞ったトレンド分析の画面表示
- 過去の予測と実際の当選番号を突き合わせた的中率トラッキング
- 抽選結果の自動取得(スクレイピングやAPI連携)
