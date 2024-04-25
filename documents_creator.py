from typing import List
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader


def get_documents(path: str) -> List:
    documents = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    for filename in os.listdir(path):
        if filename.endswith('.txt'):
            file_path = os.path.join(path, filename)
            loader = TextLoader(file_path, encoding="utf-8")
            document = loader.load()
            documents.extend(text_splitter.split_documents(document))

    return documents
