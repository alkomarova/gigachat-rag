import os

from langchain.chains import RetrievalQA
from langchain.chat_models.gigachat import GigaChat
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS

from typing import List, Tuple
from template import template

TOKEN = os.getenv('GCTOKEN')


def run_chain(db: FAISS, question: str) -> Tuple[str, set]:
    model = GigaChat(credentials=TOKEN, verify_ssl_certs=False,
                     scope='GIGACHAT_API_CORP')
    prompt = PromptTemplate(
        input_variables=["context", "question"], template=template)

    similar_chanks = db.similarity_search(question, k=3)
    unique_sources = set(chank.metadata['source'].split(
        '/')[-1].split('.')[0] for chank in similar_chanks)
    retriever = db.as_retriever(search_kwargs={"k": 3})

    qa = RetrievalQA.from_chain_type(llm=model,
                                     chain_type_kwargs={"prompt": prompt},
                                     retriever=retriever)
    result = qa.invoke({"query": question})
    return result['result'], unique_sources
