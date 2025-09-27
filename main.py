"""
@file main.py
@brief Multi-language PDF viewer with password management (py-pdf-viewer)
@details
    - PDF表示（GUI）
    - パスワード付きPDFの開封・設定・変更
    - 英語・日本語・中国語対応
    - PyPDF2, PyMuPDF, Pillow, tkinter使用
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
    @brief PDFビュワーのメインアプリケーション
    @details GUI構築・PDF操作・多言語切替を担当
    """

    def __init__(self, root, lang="en"):
        """
        @brief コンストラクタ
        @param root Tkinterのrootウィンドウ
        @param lang 言語コード（"en", "ja", "zh"）
        """
        self.root = root
        self.lang = lang
        self.locale = self.load_locale(lang)
        self.root.title("PDF Viewer")
        self.pdf_path = None
        self.pdf_password = None
        self.page_images = []
        self.current_page = 0
        self.setup_ui()

    def load_locale(self, lang):
        """
        @brief ロケールファイルを読み込む
        @param lang 言語コード
        @return 辞書型のロケールデータ
        """
        locale_path = os.path.join(os.path.dirname(__file__), "locale", f"{lang}.json")
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
        """
        @brief GUI部品の初期化
        """
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
        """
        @brief PDFファイルを開いて表示
        パスワード付きPDFの場合は入力を促す
        """
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not path:
            return
        self.pdf_path = path
        try:
            doc = fitz.open(path)
        except RuntimeError:
            password = simpledialog.askstring(
                self.locale["open"], self.locale["password_prompt"], show="*"
            )
            if not password:
                messagebox.showerror(
                    self.locale["error"], self.locale["password_required"]
                )
                return
            try:
                doc = fitz.open(path, password=password)
                self.pdf_password = password
            except Exception:
                messagebox.showerror(
                    self.locale["error"], self.locale["password_incorrect"]
                )
                return
        self.page_images = []
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            self.page_images.append(img)
        self.current_page = 0
        self.show_page()

    def show_page(self):
        """
        @brief 現在ページのPDF画像を表示
        """
        if not self.page_images:
            return
        img = self.page_images[self.current_page]
        img = img.resize((600, 800))
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)

    def prev_page(self):
        """
        @brief 前のページを表示
        """
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()

    def next_page(self):
        """
        @brief 次のページを表示
        """
        if self.current_page < len(self.page_images) - 1:
            self.current_page += 1
            self.show_page()

    def set_password(self):
        """
        @brief PDFファイルに新しいパスワードを設定
        """
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not path:
            return
        password = simpledialog.askstring(
            self.locale["set_password"], self.locale["password_set_prompt"], show="*"
        )
        if not password:
            messagebox.showerror(self.locale["error"], self.locale["password_required"])
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
            messagebox.showinfo(self.locale["done"], self.locale["password_set_done"])

    def change_password(self):
        """
        @brief PDFファイルのパスワードを変更
        """
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not path:
            return
        old_password = simpledialog.askstring(
            self.locale["change_password"],
            self.locale["password_change_prompt"],
            show="*",
        )
        if not old_password:
            messagebox.showerror(self.locale["error"], self.locale["password_required"])
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
            messagebox.showerror(self.locale["error"], self.locale["password_required"])
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
    """
    @brief アプリケーションのエントリポイント
    @details コマンドライン引数で言語指定可能
    """
    import sys

    lang = "en"
    if len(sys.argv) > 1 and sys.argv[1] in ["en", "ja", "zh"]:
        lang = sys.argv[1]
    root = tk.Tk()
    app = PDFViewerApp(root, lang=lang)
    root.mainloop()


if __name__ == "__main__":
    main()
