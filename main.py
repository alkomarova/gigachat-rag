from chain import run_chain
from documents_creator import get_documents, get_database
from pdf_parser import pdf_to_txt


def main():
    pdf_to_txt('data/')
    documents = get_documents('parsed_data/')
    db = get_database(documents)
    print('Задайте свой вопрос, если вопросы закончились, напишите: Stop')
    question = input()
    while question != 'Stop':
        result, sources = run_chain(db, question)
        print(result)
        if len(sources) and result != 'Я не знаю.':
            print('Использованные источники:', ', '.join(map(str, sources)))
        print('Еще вопросы?')
        question = input()


if __name__ == "__main__":
    main()
