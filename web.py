from chain import get_chat_response
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
        return get_chat_response(data['message'])
    else:
        # Если поле 'message' отсутствует, возвращаем ошибку
        return 'Ошибка: поле "message" отсутствует в запросе', 400

if __name__ == '__main__':
    app.run(debug=True)
