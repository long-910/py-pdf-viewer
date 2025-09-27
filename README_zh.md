# py-pdf-viewer

## 概述

py-pdf-viewer 是用 Python 编写的简单 PDF 查看器。支持查看加密 PDF、设置和更改 PDF 密码。

## 主要功能

- 查看 PDF 文件（GUI）
- 打开加密 PDF 时提示输入密码
- 设置 PDF 文件密码
- 更改 PDF 文件密码

## 所需库

- PyPDF2
- PyMuPDF
- Pillow
- tkinter（标准库）

## 安装方法

1. 安装 Python 3.8 或更高版本。
2. 安装所需库：
   ```powershell
   pip install -r requirements.txt
   ```

## 使用方法

1. 启动应用程序：
   ```powershell
   python main.py
   ```
   或指定语言：
   ```powershell
   python main.py zh   # 中文
   python main.py en   # 英文
   python main.py ja   # 日文
   ```
2. 使用菜单打开 PDF 文件。
3. 如果 PDF 受密码保护，将弹出密码输入框。
4. 在“文件”菜单中设置或更改密码。

## 文档

详细用法请参见 `docs/USAGE.md`。

## 许可证

MIT License
