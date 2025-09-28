"""
@file main.py.

@brief Multi-language PDF viewer with password management (py-pdf-viewer).

@details
    - PDF表示（GUI）
    - パスワード付きPDFの開封・設定・変更
    - 英語・日本語・中国語対応
    - PyPDF2, PyMuPDF, Pillow, tkinter使用.
"""

import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import os
import json


class PDFViewerApp:
    """
    @brief PDFビュワーのメインアプリケーション.

    @details GUI構築・PDF操作・多言語切替を担当.
    """

    def __init__(self, root, lang="en", debug=False):
        """コンストラクタ."""
        self.root = root
        self.lang = lang
        self.locale = self.load_locale(lang)
        self.root.title("PDF Viewer")
        self.pdf_path = None
        self.pdf_password = None
        self.page_images = []
        self.current_page = 0
        self.debug = debug
        self.setup_ui()

    def debug_log(self, msg):
        """デバッグログ出力."""
        if self.debug:
            print(f"[DEBUG] {msg}")

    def load_locale(self, lang):
        """ロケールファイルを読み込む."""
        locale_path = os.path.join(
            os.path.dirname(__file__), "locale", f"{lang}.json"
        )
        try:
            with open(locale_path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            with open(
                os.path.join(os.path.dirname(__file__), "locale", "en.json"),
                encoding="utf-8",
            ) as f:
                return json.load(f)

    def setup_ui(self):
        """GUI部品の初期化."""
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label=self.locale["open"], command=self.open_pdf)
        file_menu.add_command(
            label=self.locale["set_password"], command=self.set_password
        )
        file_menu.add_command(
            label=self.locale["change_password"], command=self.change_password
        )
        menubar.add_cascade(label=self.locale["file"], menu=file_menu)
        self.root.config(menu=menubar)

        self.canvas = tk.Canvas(self.root, width=600, height=800)
        self.canvas.pack()

        nav_frame = tk.Frame(self.root)
        nav_frame.pack()
        self.prev_btn = tk.Button(
            nav_frame, text=self.locale["prev_page"], command=self.prev_page
        )
        self.prev_btn.pack(side=tk.LEFT)
        self.next_btn = tk.Button(
            nav_frame, text=self.locale["next_page"], command=self.next_page
        )
        self.next_btn.pack(side=tk.LEFT)

    def open_pdf(self):
        """PDFファイルを開いて表示する。パスワード付きPDFの場合は入力を促す."""
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not path:
            self.debug_log("PDFファイル選択キャンセル")
            return
        self.pdf_path = path
        self.debug_log(f"PDFファイル選択: {path}")
        doc = None
        password = None
        while True:
            try:
                if password:
                    self.debug_log(
                        f"パスワード指定でPDFオープン再試行: {password}"
                    )
                    doc = fitz.open(path, password=password)
                else:
                    self.debug_log("パスワードなしでPDFオープン試行")
                    doc = fitz.open(path)
                # ページを開いてみて暗号化エラーを検出
                _ = doc.load_page(0)
                self.debug_log("PDFオープン成功")
                break
            except (RuntimeError, ValueError):
                self.debug_log("PDFオープン失敗: パスワード要求")
                password = simpledialog.askstring(
                    self.locale["open"],
                    self.locale["password_prompt"],
                    show="*",
                )
                if not password:
                    self.debug_log("パスワード入力キャンセル")
                    messagebox.showerror(
                        self.locale["error"], self.locale["password_required"]
                    )
                    return
            except Exception:
                self.debug_log(
                    "PDFオープン失敗: パスワード不正またはその他エラー"
                )
                messagebox.showerror(
                    self.locale["error"], self.locale["password_incorrect"]
                )
                return
        self.pdf_password = password
        self.page_images = []
        self.debug_log(f"ページ数: {doc.page_count}")
        for page_num in range(doc.page_count):
            self.debug_log(f"ページ読込: {page_num}")
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            self.page_images.append(img)
        self.current_page = 0
        self.debug_log("最初のページ表示")
        self.show_page()

    def show_page(self):
        """現在ページのPDF画像を表示する."""
        if not self.page_images:
            self.debug_log("ページ画像なし")
            return
        img = self.page_images[self.current_page]
        img = img.resize((600, 800))
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
        self.debug_log(f"ページ表示: {self.current_page}")

    def prev_page(self):
        """前のページを表示する."""
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()

    def next_page(self):
        """次のページを表示する."""
        if self.current_page < len(self.page_images) - 1:
            self.current_page += 1
            self.show_page()

    def set_password(self):
        """PDFファイルに新しいパスワードを設定する."""
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not path:
            return
        password = simpledialog.askstring(
            self.locale["set_password"],
            self.locale["password_set_prompt"],
            show="*",
        )
        if not password:
            messagebox.showerror(
                self.locale["error"], self.locale["password_required"]
            )
            return
        reader = PdfReader(path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(password)
        out_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )
        if out_path:
            with open(out_path, "wb") as f:
                writer.write(f)
            messagebox.showinfo(
                self.locale["done"], self.locale["password_set_done"]
            )

    def change_password(self):
        """PDFファイルのパスワードを変更する."""
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not path:
            return
        old_password = simpledialog.askstring(
            self.locale["change_password"],
            self.locale["password_change_prompt"],
            show="*",
        )
        if not old_password:
            messagebox.showerror(
                self.locale["error"], self.locale["password_required"]
            )
            return
        reader = PdfReader(path)
        try:
            reader.decrypt(old_password)
        except Exception:
            messagebox.showerror(
                self.locale["error"], self.locale["password_incorrect"]
            )
            return
        new_password = simpledialog.askstring(
            self.locale["change_password"],
            self.locale["password_change_new_prompt"],
            show="*",
        )
        if not new_password:
            messagebox.showerror(
                self.locale["error"], self.locale["password_required"]
            )
            return
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(new_password)
        out_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )
        if out_path:
            with open(out_path, "wb") as f:
                writer.write(f)
            messagebox.showinfo(
                self.locale["done"], self.locale["password_change_done"]
            )


def main():
    """アプリケーションのエントリポイント。コマンドライン引数で言語指定可能."""
    import sys

    lang = "en"
    debug = False
    for arg in sys.argv[1:]:
        if arg in ["en", "ja", "zh"]:
            lang = arg
        if arg == "--debug":
            debug = True
    root = tk.Tk()
    PDFViewerApp(root, lang=lang, debug=debug)
    root.mainloop()


if __name__ == "__main__":
    main()
