import os
import sys
import chardet
from ebooklib import epub

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)
        result = chardet.detect(raw_data)
        return result['encoding']

def txt_to_epub(txt_file_path, output_path=None):
    if not os.path.exists(txt_file_path):
        print("TXT 文件不存在")
        return

    # 自动检测文件编码
    encoding = detect_encoding(txt_file_path)
    print(f"检测到编码：{encoding}")

    with open(txt_file_path, 'r', encoding=encoding, errors='ignore') as f:
        text = f.read()

    html_text = text.replace("\n", "<br/>")

    book = epub.EpubBook()
    book.set_identifier("id123456")
    book.set_title("Converted Book")
    book.set_language("zh")
    book.add_author("Auto Converter")

    chapter = epub.EpubHtml(title='Chapter 1', file_name='chap_01.xhtml', lang='zh')
    chapter.content = f'<h1>Chapter 1</h1><p>{html_text}</p>'
    book.add_item(chapter)
    book.toc = (epub.Link('chap_01.xhtml', 'Chapter 1', 'chap1'),)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.spine = ['nav', chapter]
    if not output_path:
        output_path = txt_file_path.replace('.txt', '.epub')
    epub.write_epub(output_path, book)
    print(f"EPUB 文件已生成：{output_path}")

if __name__ == "__main__":
    for file in os.listdir("."):
        if file.endswith(".txt"):
            txt_to_epub(file)
