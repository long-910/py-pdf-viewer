"""PDFユーティリティのテストモジュール."""

import os
import tempfile
from PyPDF2 import PdfWriter, PdfReader


def create_sample_pdf(path):
    """サンプルPDFを作成する."""
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with open(path, "wb") as f:
        writer.write(f)


def test_set_password():
    """PDFにパスワードを設定し、正しく開けるかテストする."""
    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, "sample.pdf")
        create_sample_pdf(pdf_path)
        password = "testpass"
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(password)
        out_path = os.path.join(tmpdir, "protected.pdf")
        with open(out_path, "wb") as f:
            writer.write(f)
        # パスワードで開けるか確認
        reader2 = PdfReader(out_path)
        result = reader2.decrypt(password)
        assert result in [1, 2]  # PyPDF2の仕様変更対応


def test_change_password():
    """PDFのパスワードを変更し、新しいパスワードで開けるかテストする."""
    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, "sample.pdf")
        create_sample_pdf(pdf_path)
        old_password = "oldpass"
        new_password = "newpass"
        # まずパスワード設定
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(old_password)
        protected_path = os.path.join(tmpdir, "protected.pdf")
        with open(protected_path, "wb") as f:
            writer.write(f)
        # パスワード変更
        reader2 = PdfReader(protected_path)
        result = reader2.decrypt(old_password)
        assert result in [1, 2]  # PyPDF2の仕様変更対応
        writer2 = PdfWriter()
        for page in reader2.pages:
            writer2.add_page(page)
        writer2.encrypt(new_password)
        changed_path = os.path.join(tmpdir, "changed.pdf")
        with open(changed_path, "wb") as f:
            writer2.write(f)
        # 新しいパスワードで開けるか
        reader3 = PdfReader(changed_path)
        result2 = reader3.decrypt(new_password)
        assert result2 in [1, 2]  # PyPDF2の仕様変更対応
