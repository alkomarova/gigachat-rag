import os

from langchain.chains import RetrievalQA
from langchain.chat_models.gigachat import GigaChat
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from arxive_api import ArxivRetriever
from langchain.chains import LLMChain
from typing import List, Tuple
from template import template
from langchain.memory import ConversationBufferMemory

from template import main_template, retriever_template

TOKEN = os.getenv('GCTOKEN')

llm = GigaChat(credentials=TOKEN,
               model="GigaChat-Pro",
               verify_ssl_certs=False,
               scope='GIGACHAT_API_CORP')
prompt = PromptTemplate(
        input_variables=["question"], template=main_template)
memory = ConversationBufferMemory(memory_key="chat_history")
chain = LLMChain(llm=llm, prompt=prompt, memory=memory)



def run_chain(documents: List, question: str) -> Tuple[str, set]:
    '''
    Старая версия с локальным сохранением данных
    '''
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


def run_chain_arxiv(question):
    retriever = ArxivRetriever(load_max_docs=3)
    qa = ConversationalRetrievalChain.from_llm(
        llm, retriever=retriever, rephrase_question=False)
    chat_history = []

    result = qa.invoke(
        {"question": question, "chat_history": chat_history})
    docs = retriever.get_relevant_documents(question)
    chat_history.append((question, result["answer"]))
    return result
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

# функция которая должна давать ответ на запрос UI
def get_chat_response(question):
    global chain, memory, llm
    result = chain.invoke(
        {"question": question, "chat_history": memory})
    print('Ответ на главный темплейт:', result)
    # для перефразирования если слабый вопрос
    counter = 0
    while '[PEREPHRASE]' in result['text'] and counter < 2:
        counter += 1
        result['text'] = result['text'].replace("[PEREPHRASE]", "")
        result['text'] = result['text'].replace("PEREPHRASE", "")
        result = run_chain_arxiv(result['text'])
        print('Что выдал архив:', result)
        add_prompt = PromptTemplate(
            input_variables=["question"], template=retriever_template)
        chain_additional = LLMChain(llm=llm, prompt=add_prompt,
                            memory=memory)
        result = chain_additional.invoke(
            {"question": result["answer"], "chat_history": memory})
        print('После того, как посмотрели на ответ архива:', result)
    if "answer" not in result:
        result["answer"] = result["text"]
    counter = 0
    return result["answer"]

# запустить CLI
def main_chats():
    question = ""
    while question != 'STOP':
        question = input()
        print(get_chat_response(question))

# пример использования функции
# print(get_chat_response("как дела?"))