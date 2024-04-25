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

from template import main_template, retriever_template, out_of_counts_template

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
    '''
    print(f"-> **Question**: {question} \n")
    print(f"**Answer**: {result['answer']} \n")
    if len(docs):
        print("Использованные источники:")
        names = set()
        for idx, doc in enumerate(docs):
            name = f'"{doc.metadata["Title"]}\". {doc.metadata["Authors"]}. {
                doc.metadata["Journal"] or ""} {doc.metadata["Published"].year}. (URL : {doc.metadata["Link"]})'
            if name not in names:
                names.add(name)
                print(f'{idx}. {name}')
    '''
    return result


def get_chat_response(question):
    global chain, memory, llm
    result = chain.invoke(
        {"question": question, "chat_history": memory})
    print('Ответ на главный темплейт:', result)
    # для перефразирования если слабый вопрос
    counter = 0
    max_counter = 2
    while '[PEREPHRASE]' in result['text'] and counter < max_counter:
        counter += 1
        perephrased_question = result['text'].replace("[PEREPHRASE]", "")
        result = run_chain_arxiv(perephrased_question)
        print('Что выдал архив:', result)
        add_prompt = PromptTemplate(
            input_variables=["question", "arxiv_answer"], template=retriever_template)
        chain_additional = LLMChain(llm=llm, prompt=add_prompt)
        result = chain_additional.invoke(
            {"question": perephrased_question, "arxiv_answer": result['answer']})
        print('После того, как посмотрели на ответ архива:', result)
    if counter >= max_counter:
        out_prompt = PromptTemplate(
            input_variables=["question"], template=out_of_counts_template)
        chain_max_counter = LLMChain(llm=llm, prompt=out_prompt)
        result = chain_max_counter.invoke(
            {"question": result['text'], "chat_history": memory})
    return result["text"]


def main_chats():
    question = ""
    while question != 'STOP':
        question = input()
        print(get_chat_response(question))
