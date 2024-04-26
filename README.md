# ScienceRAG + GigaChat

## Описание проекта
ScienceRAG + GigaChat — это чат-бот, основанный на системе RAG (Retrieval-Augmented Generation), специализирующийся на ответах на узкоспециализированные научные вопросы.

## Как работает бот?
1. **Автоматический ответ:** На начальном этапе бот пытается ответить на вопрос пользователя с помощью встроенной базы знаний.
2. **Поиск научных статей:** Если бот не уверен в ответе, он обращается к сайту Arxiv.org для поиска наиболее релевантных научных статей.
3. **Анализ статей:** Статьи разбиваются на фрагменты, которые анализируются на предмет близости к заданному вопросу на основе векторного расстояния.
4. **Генерация ответа:** Бот генерирует ответ, опираясь на контекст наиболее релевантных фрагментов.
5. **Переформулировка ответа:** Если ответ кажется неполным, бот переформулирует его несколько раз для улучшения качества.
6. **Финальный ответ:** Если переформулировка успешна, бот выдает окончательный ответ, основанный на всех проанализированных документах. Если нет — предоставляется лучший возможный ответ, сгенерированный на основе своих внутренних знаний.

## Начало работы
Перед запуском проекта необходимо выполнить ряд подготовительных шагов для корректной работы бота.

### Установка токена
Для начала нужно задать переменную окружения `GCTOKEN`, содержащую ваш токен доступа. Это делается следующим образом:

#### Windows
Откройте командную строку и введите:
```bash
setx GCTOKEN "Ваш_Токен_Здесь"
```
#### macOS
Откройте терминал и выполните команду:
```bash
export GCTOKEN="Ваш_Токен_Здесь"
```
### Установка зависимостей
Установите все библиотеки из файла requirements.txt
### Запуск проекта
После установки переменной окружения запустите команду `python web.py`, затем перейдите в папку проекта и запустите файл `ui.html`.
