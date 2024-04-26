import os

from langchain.chains import RetrievalQA
from langchain.chat_models.gigachat import GigaChat
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from arxive_api import ArxivRetriever
from langchain.chains import LLMChain
from typing import List, Tuple, Dict
from langchain.memory import ConversationBufferMemory

from template import *

TOKEN = os.getenv('GCTOKEN')

llm = GigaChat(credentials=TOKEN,
               model="GigaChat-Pro",
               verify_ssl_certs=False,
               scope='GIGACHAT_API_CORP')
prompt = PromptTemplate(
    input_variables=["question"], template=main_template)
memory = ConversationBufferMemory(memory_key="chat_history")
chain = LLMChain(llm=llm, prompt=prompt, memory=memory)


def run_chain_arxiv(question):
    retriever = ArxivRetriever(load_max_docs=3)
    qa = ConversationalRetrievalChain.from_llm(
        llm, retriever=retriever, rephrase_question=False)
    chat_history = []

    result = qa.invoke(
        {"question": question, "chat_history": chat_history})
    docs = retriever.get_relevant_documents(question)
    chat_history.append((question, result["answer"]))
    
    # list_of_sources = None
    # if len(docs):
    #     list_of_sources = "Список источников, по которым шел поиск: \n"
    #     names = set()
    #     for idx, doc in enumerate(docs):
    #         name = f'"{doc.metadata["Title"]}\". {doc.metadata["Authors"]}. {
    #             doc.metadata["Journal"] or ""} {doc.metadata["Published"].year}. (URL : {doc.metadata["Link"]})'
    #         if name not in names:
    #             names.add(name)
    #             list_of_sources.append(f'{idx}. {name}')
    
    return result

def _check_need_arxive(result):
    add_prompt = PromptTemplate(
            input_variables=["gigachat_answer"], template=template_need_arxive)
    chain_additional = LLMChain(llm=llm, prompt=add_prompt)
    res = chain_additional.invoke({"gigachat_answer":result["text"]})
    print("_check_need_arxive: ", res)
    return res["text"]

def _rewrite_query_arxive(question, review_marks):
    add_prompt = PromptTemplate(
            input_variables=["question", "review_marks"], template=arxive_rewrite_tempalte)
    chain_additional = LLMChain(llm=llm, prompt=add_prompt)
    result = chain_additional.invoke({"question": question, "review_marks": review_marks})
    print("_rewrite_query_arxive: ", result)
    return result["text"]

def _check_arxive_helps(question, arxive_answer):
    add_prompt = PromptTemplate(
        input_variables=["question", "arxiv_answer"], template=arxive_evaluate_template)
    chain_additional = LLMChain(llm=llm, prompt=add_prompt)
    result = chain_additional.invoke({"question": question, "arxiv_answer": arxive_answer})
    print("_check_arxive_helps: ", result)
    return result["text"]
    
def _arxive_no_found(question):
    add_prompt = PromptTemplate(
        input_variables=["question"], template=out_of_counts_template)
    chain_additional = LLMChain(llm=llm, prompt=add_prompt)
    result = chain_additional.invoke({"question": question})
    print("_arxive_no_found_: ", result)
    return result["text"]

def get_chat_response(question):
    global chain, memory, llm
    result = chain.invoke(
        {"question": question, "chat_history": memory})
    print('Ответ на главный темплейт:', result)
    final_answer = None

    is_need_arxive = _check_need_arxive(result)

    if (is_need_arxive.find("NO") != -1):
        # для перефразирования если слабый вопрос
        print("Lets go deep to Arxive")
        counter = 0
        max_counter = 2
        question_arxiv = question
        while counter < max_counter:
            counter += 1
            result = run_chain_arxiv(question_arxiv)
            arxive_result = result["answer"]
            print('Что выдал архив:', result)
            answer_review = _check_arxive_helps(question, arxive_result)
            if (answer_review.find("NO")!=-1):
                question_arxiv = _rewrite_query_arxive(question, answer_review)
            else:
                final_answer = arxive_result
                break
        if (final_answer is None):
            final_answer = _arxive_no_found(question)
    else:
        final_answer = result["text"]
    return final_answer


def main_chats():
    question = ""
    while question != 'STOP':
        question = input()
        print(get_chat_response(question))
