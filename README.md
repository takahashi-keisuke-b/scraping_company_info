# 会社概要クローラー（スクレイピングツール）

[![CI](https://github.com/takahashi-keisuke-b/scraping_company_info/actions/workflows/CI.yml/badge.svg)](https://github.com/takahashi-keisuke-b/scraping_company_info/actions/workflows/CI.yml)

ターゲットとなる企業サイトのURLを入力するだけで、サイト内を自律的に巡回（クローリング）し、会社概要ページから自動で企業情報を抽出するPythonアプリケーションです。

実務での保守性・拡張性を意識し、クリーンアーキテクチャ（レイヤードアーキテクチャ）およびドメイン駆動設計（DDD）の思想を取り入れて強固に設計しています。

---

## 特徴とこだわり

### 1. 堅牢なアーキテクチャ設計（クリーンアーキテクチャ / DDD）
単に動くスクレイピングコードを書くのではなく、ビジネスロジックと外部依存（UI、ネットワーク通信）を完全に分離しています。
- **Domain（ドメイン層）**: `Company`, `Url`, `Html` など、ビジネスルールを純粋な値オブジェクト/エンティティとしてカプセル化（`dataclass(frozen=True)` によるイミュータブルな設計）。
- **UseCase（ユースケース層）**: `CrawlCompanyUseCase` に巡回アルゴリズムを集約。
- **WebController（インフラ・表現層）**: HTTP通信（`requests`）やHTML解析（`BeautifulSoup`）を独立させ、仕様変更に強い構造にしています。

### 2. 高精度な優先度付きクローリングアルゴリズム
無駄なページ遷移を減らすため、リンクテキストやURLのディレクトリ階層（「company」「about」など）から「会社概要ページである確率」を動的にスコアリングします。スコアの高いURLから優先的に探索する、賢い巡回ロボットを搭載しています。

### 3. テーブル＆DLタグのハイブリッド抽出
多くの企業サイトで採用されている `<table>` タグだけでなく、`<dl><dt><dd>` タグによる会社概要の構造にも対応。キーワードマッチング（`Company_Key.py`）により、表記揺れがあっても高い精度で情報をマッピングします。

### 4. 万全なエラーハンドリング（独自Result型）
例外（Exception）を呼び出し元に投げてアプリをクラッシュさせるのではなく、関数型プログラミングの思想を取り入れた独自の `Result` 型で成否を管理。不安定なWebスクレイピングにおいても、システム全体の安定性を保証しています。

---

## 技術スタック
- **Language**: Python 3.10+
- **Framework (UI)**: Streamlit (Web UI)
- **Libraries**: Requests, BeautifulSoup4

---

## フォルダ構成

```
.
├── config/
│   └── Company_Key.py        # 巡回・抽出用のキーワード定義
├── domain/
│   ├── Company.py            # 企業情報のデータ構造
│   ├── Html.py               # HTML値オブジェクト
│   └── Url.py                # URL値オブジェクト（ドメイン検証付）
├── usecase/
│   └── CrawlCompanyUseCase.py # 優先度付き巡回・探索ロジック
├── util/
│   └── Result.py             # エラーハンドリング用Resultラッパー
├── web_controller/
│   ├── base_html_mapper.py   # BeautifulSoupの汎用マッパー
│   ├── company_html_mapper.py # 企業情報・URLスコアリング特化マッパー
│   └── http_client.py        # ポリシー（Politeness）を考慮した通信クライアント
├── scraping_site_01.py       # Streamlit Webアプリケーション（エントリーポイント）
└── .gitignore                # 不要ファイル（__pycache__等）の除外設定
```