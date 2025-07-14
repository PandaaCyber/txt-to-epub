import os
import re
import chardet
from ebooklib import epub

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)
        result = chardet.detect(raw_data)
        return result['encoding']

def split_into_chapters(text):
    # 匹配「第1章」、「第十二章」这种
    chapters = re.split(r'(第[\d一二三四五六七八九十百千]+章.*?)\n', text)
    result = []
    if not chapters or len(chapters) < 3:
        return [("正文", text)]
    for i in range(1, len(chapters) - 1, 2):
        title = chapters[i].strip()
        content = chapters[i + 1].strip().replace("\n", "<br/>")
        result.append((title, content))
    return result

def txt_to_epub(txt_file_path, output_path=None):
    if not os.path.exists(txt_file_path):
        print("TXT 文件不存在")
        return

    encoding = detect_encoding(txt_file_path)
    print(f"检测到编码：{encoding}")

    with open(txt_file_path, 'r', encoding=encoding, errors='ignore') as f:
        lines = f.readlines()

    if not lines:
        print("TXT 文件为空")
        return

    title = lines[0].strip() or "电子书"
    text = ''.join(lines[1:])

    book = epub.EpubBook()
    book.set_identifier("id123456")
    book.set_title(title)
    book.set_language("zh")
    book.add_author("Auto Converter")

    # 设置封面（默认使用网络图片链接）
with open("cover.jpg", "rb") as f:
    book.set_cover("cover.jpg", f.read())



    chapters = split_into_chapters(text)
    epub_chapters = []

    for i, (ch_title, ch_content) in enumerate(chapters):
        chapter = epub.EpubHtml(title=ch_title, file_name=f'chap_{i+1}.xhtml', lang='zh')
        chapter.content = f'<h2>{ch_title}</h2><p>{ch_content}</p>'
        book.add_item(chapter)
        epub_chapters.append(chapter)

    book.toc = tuple(epub_chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav'] + epub_chapters

    if not output_path:
        output_path = txt_file_path.replace('.txt', '.epub')
    epub.write_epub(output_path, book)
    print(f"✅ EPUB 已生成：{output_path}")

if __name__ == "__main__":
    import requests
    for file in os.listdir("."):
        if file.endswith(".txt"):
            txt_to_epub(file)
