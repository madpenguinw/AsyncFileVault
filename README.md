# Обращение к ревьюверу в файле TO_REVIEWER.txt


# Проектное задание пятого спринта

Вам необходимо спроектировать и разработать файловое хранилище, которое позволяет хранить различные типы файлов — документы, фотографии, другие данные.

Кроме этого, выберите и реализуйте из списка дополнительные требования. У каждого требования есть определённая сложность, от которой зависит количество баллов. Необходимо выбрать такое количество заданий, чтобы общая сумма баллов больше или равна 2. Выбор заданий никак не ограничен: можно выбрать все простые или одно среднее и два простых, или одно продвинутое, или решить все.

## Описание задания

Реализовать **http-сервис**, который обрабатывает поступающие запросы. Сервер стартует по адресу `http://127.0.0.1:8080` (дефолтное значение, можнть быть изменено).

<details>
<summary> Список необходимых эндпойнтов </summary>

1. Статус активности связанных сервисов

```
GET /ping
```
Получить информацию о времени доступа ко всем связанным сервисам, например, к БД, кэшам, примонтированным дискам и т.д.

**Response**
```json
{
    "db": 1.27,
    "cache": 1.89,
    ...
    "service-N": 0.56
}
```

2. Регистрация пользователя.

```
POST /register
```
Регистрация нового пользователя. Запрос принимает на вход логин и пароль для создания новой учетной записи.


3. Авторизация пользователя.

```
POST /auth
```
Запрос принимает на вход логин и пароль учетной записи и возвращает авторизационный токен. Далее все запросы проверяют наличие токена в заголовках - `Authorization: Bearer <token>`


4. Информация о загруженных файлах

```
GET /files/
```
Вернуть информацию о ранее загруженных файлах. Доступно только авторизованному пользователю.

**Response**
```json
{
    "account_id": "AH4f99T0taONIb-OurWxbNQ6ywGRopQngc",
    "files": [
          {
            "id": "a19ad56c-d8c6-4376-b9bb-ea82f7f5a853",
            "name": "notes.txt",
            "created_ad": "2020-09-11T17:22:05Z",
            "path": "/homework/test-fodler/notes.txt",
            "size": 8512,
            "is_downloadable": true
          },
        ...
          {
            "id": "113c7ab9-2300-41c7-9519-91ecbc527de1",
            "name": "tree-picture.png",
            "created_ad": "2019-06-19T13:05:21Z",
            "path": "/homework/work-folder/environment/tree-picture.png",
            "size": 1945,
            "is_downloadable": true
          }
    ]
}
```


5. Загрузить файл в хранилище

```
POST /files/upload
```
Метод загрузки файла в хранилище. Доступно только авторизованному пользователю.
Для загрузки заполняется полный путь до файла, в который будет загружен/переписан загружаемый файл. Если нужные директории не существуют, то они должны быть созданы автоматически.
Так же, есть возможность указать только путь до директории. В этом случае имя создаваемого файла будет создано в соответствии с передаваемым именем файла.

**Request**
```
{
    "path": <full-path-to-file>||<path-to-folder>,
}
```

**Response**
```json
{
    "id": "a19ad56c-d8c6-4376-b9bb-ea82f7f5a853",
    "name": "notes.txt",
    "created_ad": "2020-09-11T17:22:05Z",
    "path": "/homework/test-fodler/notes.txt",
    "size": 8512,
    "is_downloadable": true
}
```


6. Скачать загруженный файл

```
GET /files/download
```
Скачивание ранее загруженного файла. Доступно только авторизованному пользователю.

**Path parameters**
```
/?path=<path-to-file>||<file-meta-id>
```
Возможность скачивания есть как по переданному пути до файла, так и по идентификатору.

</details>


## Дополнительные требования (отметьте [X] выбранные пункты):

- [ ] (2 балла) Добавление возможности скачивания в архиве

<details>
<summary> Описание изменений </summary>

```
GET /files/download
```
Path-параметр расширяется дополнительным параметром - `compression`. Доступно только авторизованному пользователю.

Дополнительно в `path` можно указать как путь до директории, так и его **UUID**. При скачивании директории будут скачиваться все файлы, находящиеся в нем.

**Path parameters**
```
/?path=[<path-to-file>||<file-meta-id>||<path-to-folder>||<folder-meta-id>] & compression"=[zip||tar||7z]
```
</details>

- [X] (2 балла) Добавление информация об использовании пользователем дискового пространства.

<details>
<summary> Описание изменений </summary>

```
GET /user/status
```
Вернуть информацию о статусе использования дискового пространства и ранее загруженных файлах. Доступно только авторизованному пользователю.

**Response**
```json
{
    "account_id": "taONIb-OurWxbNQ6ywGRopQngc",
    "info": {
        "root_folder_id": "19f25-3235641",
        "home_folder_id": "19f25-3235641"
    },
    "folders": [
        "root": {
            "allocated": "1000000",
            "used": "395870",
            "files": 89
        },
        "home": {
            "allocated": "1590",
            "used": "539",
            "files": 19
        },
        ...,
        "folder-188734": {
            "allocated": "300",
            "used": "79",
            "files": 2
      }
    ]
}
```
</details>


- [ ] (3 балла) Добавление возможности поиска файлов по заданным параметрам.

<details>
<summary> Описание изменений </summary>

```
POST /files/search
```
Вернуть информацию о загруженных файла в по заданным параметрам. Доступно только авторизованному пользователю.

**Request**
```json
{
    "options": {
        "path": <folder-id-to-search>,
        "extension": <file-extension>,
        "order_by": <field-to-order-search-result>,
        "limit": <max-number-of-results>
    },
    "query": "<any-text||regex>"
}
```

**Response**
```json
{
    "mathes": [
          {
            "id": "113c7ab9-2300-41c7-9519-91ecbc527de1",
            "name": "tree-picture.png",
            "created_ad": "2019-06-19T13:05:21Z",
            "path": "/homework/work-folder/environment/tree-picture.png",
            "size": 1945,
            "is_downloadable": true
          },
        ...
    ]
}
```
</details>

- [ ] (4 балла) Поддержка версионирования изменений файлов.

<details>
<summary> Описание изменений </summary>

```
POST /files/revisions
```
Вернуть информацию об изменениях файла по заданным параметрам. Доступно только авторизованному пользователю.

**Request**
```json
{
    "path": <path-to-file>||<file-meta-id>,
    "limit": <max-number-of-results>
}
```

**Response**
```json
{
    "revisions": [
          {
            "id": "b1863132-5db6-44fe-9d34-b944ab06ad81",
            "name": "presentation.pptx",
            "created_ad": "2020-09-11T17:22:05Z",
            "path": "/homework/learning/presentation.pptx",
            "size": 3496,
            "is_downloadable": true,
            "rev_id": "676ffc2a-a9a5-47f6-905e-99e024ca8ac8",
            "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "modified_at": "2020-09-21T05:13:49Z"
          },
        ...
    ]
}
```
</details>

## Требования к решению

1. В качестве СУБД используйте PostgreSQL (не ниже 10 версии).
2. Опишите [docker-compose](docker-compose.yml) для разработки и локального тестирования сервисов.
3. Используйте концепции ООП.
4. Предусмотрите обработку исключительных ситуаций.
5. Приведите стиль кода в соответствие pep8, flake8, mypy.
6. Логируйте результаты действий.
7. Покройте написанный код тестами.


## Рекомендации к решению

1. За основу решения можно взять реализацию проекта 4 спринта.
2. Используйте готовые библиотеки и пакеты, например, для авторизации. Для поиска можно использовать [сервис openbase](https://openbase.com/categories/python), [PyPi](https://pypi.org/) или на [GitHub](https://github.com/search?).
3. Используйте **in-memory-db** для кэширования данных.
4. Для скачивания файлов можно использовать возможности сервера отдачи статики, для хранения — облачное объектное хранилище (s3).


## Запуск проекта

- Клонировать репозиторий и перейти в него в командной строке.

```
git clone https://github.com/madpenguinw/async-python-sprint-5
```

- Из корневой папки проекта:

```
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
```

- Установка зависимостей из корневой папки проекта:

```
pip install -r requirements.txt
```

- создать файл .env в папке src/ с переменными окружения. Шаблон (он же находится в файле example.env):

```
PROJECT_NAME=FileManager
DATABASE_DSN=postgresql+asyncpg://postgres:postgres@localhost:5432/postgres
PROJECT_PORT=8080
PROJECT_HOST=127.0.0.1
BLACKLISTED_IPS=[]
DB_PORTS=5432:5432
FM_PORTS=8080:8080
NG_PORTS=80:80
RESET_PASSWORD=SECRET_1
VERIFICATION=SECRET_2
FILES_DIR=files
```

- При добавлении IP в список BLACKLISTED_IPS (для проверки работоспособности - 127.0.0.1), доступ с него к данному ресурсу будет заблокирован
- Запустить на устройстве Docker
- Выполнить в консоли команду для запуска PostgreSQL в Docker-контейнере:

```
docker run \
  --rm   \
  --name postgres-fastapi \
  -p 5432:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=collection \
  -d postgres:15.1
```
- Для запуска сервера из папки src/ выполнить:
```
python main.py

или

uvicorn main:app --reload --port:8080
```
- Подготовить миграции:

```
alembic revision --autogenerate -m 01_initial-db
```
- Открыть файл с миграциями в папке migrations/versions (название заканчивается на 01_initial-db) и вставить строку 'import fastapi_users_db_sqlalchemy' в начало файла

- Выполнить миграции
```
alembic upgrade head
```

- Swagger доступен по адресу http://127.0.0.1:8080/api/openapi

## Об авторе

```
developed_by = {'author': 'Mikhail Sokolov',
                'university': 'ITMO',
                'courses': 'Yandex.Practicum',
                'telegram': 't.me/lmikhailsokolovl',
                'is_it_funny': 'Yes!'}
```
