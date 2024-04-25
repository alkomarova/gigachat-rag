import os
from typing import List

from langchain.callbacks.manager import CallbackManagerForRetrieverRun
from langchain_community.utilities.arxiv import ArxivAPIWrapper
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter

TOKEN = os.getenv('GCTOKEN')

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=150,
)


class ArxivRetriever(BaseRetriever, ArxivAPIWrapper):

    get_full_documents: bool = False

    def _get_relevant_documents(
            self, query: str, *, run_manager: CallbackManagerForRetrieverRun) -> List[Document]:
        try:
            import fitz
        except ImportError:
            raise ImportError(
                "PyMuPDF package not found, please install it with "
                "`pip install pymupdf`"
            )

        try:
            query = query.replace(":", "").replace("-", "")
            if self.is_arxiv_identifier(query):
                results = self.arxiv_search(
                    id_list=query[: self.ARXIV_MAX_QUERY_LENGTH].split(),
                    max_results=self.load_max_docs,
                ).results()
            else:
                results = self.arxiv_search(
                    query[: self.ARXIV_MAX_QUERY_LENGTH], max_results=self.load_max_docs
                ).results()
        except self.arxiv_exceptions as ex:
            return

        parsed_path = 'parsed_data/'
        if not os.path.exists(parsed_path):
            os.makedirs(parsed_path)
        docs = []
        for result in results:
            try:
                doc_file_name: str = result.download_pdf(
                    f'{parsed_path}{result.title}.pdf')
                with fitz.open(doc_file_name) as doc_file:
                    text: str = "".join(page.get_text() for page in doc_file)
            except (FileNotFoundError, fitz.fitz.FileDataError) as f_ex:
                continue

            metadata = {
                "Published": result.updated.date(),
                "Title": result.title,
                "Authors": ", ".join(a.name for a in result.authors),
                "Journal": result.journal_ref,
                "Link": result.pdf_url
            }

            doc = [Document(
                page_content=text[: self.doc_content_chars_max], metadata=metadata)]
            splitted = text_splitter.split_documents(doc)
            docs.extend(splitted)

        if len(docs):
            embeddings = GigaChatEmbeddings(
                credentials=TOKEN, verify_ssl_certs=False, scope='GIGACHAT_API_CORP')
            db = FAISS.from_documents(docs, embeddings)
            similar_chanks = db.similarity_search(query, k=5)
            return similar_chanks
        else:
            return []
