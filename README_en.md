# py-pdf-viewer

## Overview

py-pdf-viewer is a simple PDF viewer built with Python. It supports viewing password-protected PDFs, setting and changing PDF passwords.

## Features

- View PDF files (GUI)
- Prompt for password when opening protected PDFs
- Set password for PDF files
- Change password for PDF files

## Requirements

- PyPDF2
- PyMuPDF
- Pillow
- tkinter (standard library)

## Installation

1. Install Python 3.8 or later.
2. Install required libraries:
   ```powershell
   pip install -r requirements.txt
   ```

## Usage

1. Launch the app:
   ```powershell
   python main.py
   ```
   Or specify language:
   ```powershell
   python main.py en   # English
   python main.py ja   # Japanese
   python main.py zh   # Chinese
   ```
2. Use the menu to open a PDF file.
3. If the PDF is password-protected, a password prompt will appear.
4. Set or change password from the "File" menu.

## Documentation

See `docs/USAGE.md` for details.

## License

MIT License
