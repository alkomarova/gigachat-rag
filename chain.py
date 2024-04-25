import os

from langchain.chains import RetrievalQA
from langchain.chat_models.gigachat import GigaChat
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from arxive_api import ArxivRetriever

from typing import List, Tuple
from template import template

TOKEN = os.getenv('GCTOKEN')


def run_chain(documents: List, question: str) -> Tuple[str, set]:
    model = GigaChat(credentials=TOKEN, verify_ssl_certs=False,
                     scope='GIGACHAT_API_CORP')
    embeddings = GigaChatEmbeddings(
        credentials=TOKEN, verify_ssl_certs=False, scope='GIGACHAT_API_CORP')
    db = FAISS.from_documents(documents, embeddings)
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


def run_chain_arxiv():
    retriever = ArxivRetriever(load_max_docs=20)
    llm = GigaChat(credentials=TOKEN,
                   model="GigaChat-Pro",
                   verify_ssl_certs=False,
                   scope='GIGACHAT_API_CORP')

    assistant_system_message = """You are a helpful research assistant. \
    Lookup relevant information as needed."""

    qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever)
    chat_history = []

    print('Задайте свой вопрос!')
    question = input()
    while question != 'STOP':
        result = qa({"question": question, "chat_history": chat_history})
        docs = retriever.get_relevant_documents(question)
        chat_history.append((question, result["answer"]))
        print(f"-> **Question**: {question} \n")
        print(f"**Answer**: {result['answer']} \n")
        print("Использованные источники:")
        for idx, doc in enumerate(docs):
            print(f'{idx}. \"{doc.metadata["Title"]}\". {doc.metadata["Authors"]}. {doc.metadata["Journal"] or ""} {doc.metadata["Published"].year}. (URL : {doc.metadata["Link"]})')
        question = input()