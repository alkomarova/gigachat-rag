from chain import run_chain, run_chain_arxiv, main_chats
from documents_creator import get_documents
from pdf_parser import pdf_to_txt


def main():
    print('Задайте свой вопрос.')
    main_chats()


'''
run previour version: 

    pdf_to_txt('data/')
    documents = get_documents('parsed_data/')
    print('Задайте свой вопрос.')
    question = input()
    result, sources = run_chain(documents, question)
    print(result)
    if len(sources) and result != 'Я не знаю.':
        print('Использованные источники:', ', '.join(map(str, sources)))
'''


if __name__ == "__main__":
    main()
