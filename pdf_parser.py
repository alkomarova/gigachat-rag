from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import MarkdownTextSplitter
from pdf4llm.helpers import pymupdf_rag 
import fitz

pdf_path = "article_examples/article_example_3.pdf"

pdf_name = pdf_path.split("/")[-1].split(".")[0]

# переводит просто в текст
loader = PyMuPDFLoader(pdf_path)
chunks = loader.load()
with open(f"{pdf_name}_parsed_txt.txt", "w", encoding="utf-8") as f:
    for chunk in chunks:
        f.write(chunk.page_content)


# тут в красивый маркдаун переводит
doc = fitz.open(pdf_path)
md_text = pymupdf_rag.to_markdown(doc) 
output = open(f"{pdf_name}_parsed_markdown.md", "w", encoding="utf-8")
output.write(md_text)
output.close()
