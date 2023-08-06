import argparse
from glob import glob
from bs4 import BeautifulSoup
from shutil import unpack_archive
import tempfile

def extract_tags(filepath):
    with open(filepath) as fp:
        html_doc = fp.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        tags = soup.find_all('a')
        return tags

def list_book_chapters_from_opf(opf_content: str):
    soup = BeautifulSoup(opf_content, 'xml')
    items = soup.find_all('item')
    return [
        item.get('href')
        for item in items
        if item.get('media-type') == "application/xhtml+xml"
    ]

def get_opf_path(directory: str):
    with open(f"{directory}/META-INF/container.xml") as fp:
        soup = BeautifulSoup(fp.read(), "xml") 
        rootfile = soup.find('rootfile')
        return rootfile.get('full-path')


def list_epub_links(filepath):
    with tempfile.TemporaryDirectory() as unpack_dir:
        unpack_archive(filepath, unpack_dir, format="zip")

        opf_path = f"{unpack_dir}/{get_opf_path(unpack_dir)}"
        with open(opf_path) as fp:
            chapters = list_book_chapters_from_opf(fp.read())

        chapter_paths = [
            f"{unpack_dir}/OEBPS/{ch_path}"
            for ch_path in chapters
        ]
        for ch_path in chapter_paths:
            tags = extract_tags(ch_path)
            for tag in tags:
                _ = tag.text
                href = tag.get('href')
                if href and href.startswith('http://'):
                    print(href)


def main():
    parser = argparse.ArgumentParser(description='Extract web links from EPUB files.')
    parser.add_argument('filepath', help='EPUB filepath')
    args = parser.parse_args()

    list_epub_links(args.filepath)

