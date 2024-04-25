from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import MarkdownTextSplitter
import pymupdf4llm
import fitz
import os

parsed_path = 'parsed_data/'
if not os.path.exists(parsed_path):
    os.makedirs(parsed_path)


def pdf_to_txt(path: str) -> None:
    for filename in os.listdir(path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(path, filename)
            loader = PyMuPDFLoader(file_path)
            chunks = loader.load()
            new_filename = filename.replace('.pdf', '') + '.txt'
            with open(f"{parsed_path}{new_filename}", "w", encoding="utf-8") as f:
                for chunk in chunks:
                    f.write(chunk.page_content)


def pdf_to_md(path: str) -> None:
    for filename in os.listdir(path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(path, filename)
            doc = fitz.open(file_path)
            md_text = pymupdf4llm.to_markdown(doc)
            new_filename = filename.replace('.pdf', '') + '.md'
            with open(f"{parsed_path}{new_filename}", "w", encoding="utf-8") as f:
                f.write(md_text)
