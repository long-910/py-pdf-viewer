# py-pdf-viewer 設計書

## 概要

Python 製の多言語対応 PDF ビュワー。GUI で PDF 表示、パスワード付き PDF の開封・設定・変更が可能。

## 構成

- `main.py`: アプリ本体。GUI・PDF 操作・多言語切替
- `locale/*.json`: 各言語の UI テキスト
- `requirements.txt`: 必要ライブラリ
- `tests/`: 機能テスト
- `Doxyfile`: Doxygen 設定

## 主なクラス・関数

### PDFViewerApp

- GUI 初期化（setup_ui）
- ロケール読込（load_locale）
- PDF 表示（open_pdf, show_page, prev_page, next_page）
- パスワード設定（set_password）
- パスワード変更（change_password）

### main()

- 言語指定（コマンドライン引数）
- アプリ起動

## 多言語対応

- `locale/en.json`, `locale/ja.json`, `locale/zh.json` で UI テキストを管理
- 起動時に言語指定可能

## テスト

- `tests/test_pdf_utils.py` で PDF パスワード機能の自動テスト

## Doxygen

- `Doxyfile`で Python コードのドキュメント生成可能
- `doxygen Doxyfile` で `docs/doxygen` に HTML 出力

## 拡張性

- locale 追加で他言語対応可能
- PDF 操作は PyPDF2/PyMuPDF で拡張可能

## 注意事項

- パスワードを忘れると PDF は開けません
- 一部 PDF で正常動作しない場合あり
