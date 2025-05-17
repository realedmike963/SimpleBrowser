# Simple Browser

**Simple Browser** は PyQt6 および QtWebEngine を使用した、Windows向けのシンプルな単一ウィンドウWebブラウザです。  
User-Agent設定、ダークモード、アクセスログ（日別保存）に対応しています。
Chromeでは動作が重い、生成AIのWebUIを開く際に余計なリソースを使いたくないという場面に軽量なブラウザを探したが見当たらないので、QtWebEngineを使い生成しています。

---

## ✅ 機能概要

- 指定したホームページから起動
- `setting.ini` に記述した User-Agent を使用
- ダークモードの切り替え
- アクセスしたURLを日別ログファイル (`logs/access_YYYYMMDD.log`) に自動記録
- GPUがない環境でも動作するよう Chromium に `--disable-gpu` を設定済み

---

## 📁 構成ファイル

```
simple_browser_gpu_disabled.zip
├── main_fixed_ua_gpu_disabled.py  ← 実行用スクリプト
├── setting.ini                    ← 設定ファイル
```

---

## ⚙️ 動作に必要な環境

- Python 3.11 または互換バージョン
- Windows 10 または 11（仮想環境・RDP 環境対応済み）

### 必須ライブラリ

```bash
pip install PyQt6 PyQt6-WebEngine
```

---

## 🚀 実行方法

1. `setting.ini` を編集してホームページや User-Agent を設定します。
2. コマンドラインで以下を実行します：

```bash
python main_fixed_ua_gpu_disabled.py
```

---

## 🧾 setting.ini の設定例

```ini
[Browser]
homepage = http://127.0.0.1:7860/
dark_mode = false
user_agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64)
```

---

## 🗂️ ログ機能

- アクセスしたURLは `logs/access_YYYYMMDD.log` に記録されます。
- ログはアプリ起動時に自動作成され、365日以上前のログは自動削除されます。

---

## 📦 EXE化方法（オプション）

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main_fixed_ua_gpu_disabled.py
```

---

## 🧑‍💻 ライセンス

MIT License またはパブリックドメインとして自由にご利用ください。
