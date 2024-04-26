from chain import get_chat_response
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['POST'])
def get_random_number():
    data = request.get_json()

    if 'message' in data:
        return get_chat_response(data['message'])
    else:
        return 'Ошибка: поле "message" отсутствует в запросе', 400


if __name__ == '__main__':
    app.run(debug=True)
