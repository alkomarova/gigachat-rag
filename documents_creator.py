from typing import List
from langchain.schema.document import Document
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.gigachat import GigaChatEmbeddings

TOKEN = os.getenv('GCTOKEN')


def get_documents(path: str) -> List[Document]:
    documents = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    for filename in os.listdir(path):
        if filename.endswith('.txt'):
            file_path = os.path.join(path, filename)
            loader = TextLoader(file_path)
            document = loader.load()
            documents.extend(text_splitter.split_documents(document))

    return documents


def get_database(documents: List[Document]) -> FAISS:
    embeddings = GigaChatEmbeddings(
        credentials=TOKEN, verify_ssl_certs=False, scope='GIGACHAT_API_CORP')
    db = FAISS.from_documents(documents, embeddings)
    return db
