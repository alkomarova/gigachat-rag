from chain_web import run_chain, run_chain_arxiv
from documents_creator import get_documents
from pdf_parser import pdf_to_txt


import random
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])  # Указываем метод POST для данного маршрута
def get_random_number():
    # Получаем данные из тела POST-запроса
    data = request.get_json()
    
    # Проверяем, есть ли в данных поле 'message'
    if 'message' in data:
        return run_chain_arxiv(data['message'])
    else:
        # Если поле 'message' отсутствует, возвращаем ошибку
        return 'Ошибка: поле "message" отсутствует в запросе', 400

if __name__ == '__main__':
    app.run(debug=True)
