# py-pdf-viewer

## 概要

py-pdf-viewer は、Python で作成されたシンプルな PDF ビュワーです。パスワード付き PDF の閲覧、パスワード設定・変更機能を備えています。

## 主な機能

- PDF ファイルの表示（GUI）
- パスワード付き PDF の開封時にパスワード入力
- PDF ファイルへのパスワード設定
- PDF ファイルのパスワード変更

## 必要なライブラリ

- PyPDF2
- PyMuPDF
- Pillow
- tkinter（標準ライブラリ）

## インストール方法

1. Python 3.8 以上をインストールしてください。
2. 必要なライブラリをインストールします。
   ```powershell
   pip install -r requirements.txt
   ```

## 使い方

1. アプリを起動します。
   ```powershell
   python main.py
   ```
   または言語指定：
   ```powershell
   python main.py ja   # 日本語
   python main.py en   # 英語
   python main.py zh   # 中国語
   ```
2. メニューから PDF ファイルを開いてください。
3. パスワード付き PDF の場合、パスワード入力ダイアログが表示されます。
4. パスワード設定・変更は「ファイル」メニューから操作できます。

## ドキュメント

詳細な使い方は `docs/USAGE.md` を参照してください。

## ライセンス

MIT License
