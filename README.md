# Simbir.GO API - сервис по аренде автомобилей
Волга IT - Задание полуфинального этапа дисциплины Backend-разработка: Web API. 

>Подробности задания находится в файле [task.pdf](https://github.com/mrgick/volga-it-2023/blob/main/task.pdf).

Проект реализован на асинхронном Python 3.11 c использованием библиотек: FastApi и SqlAlchemy, а также c использованием баз данных: PostgreSQL и Redis.

## Особенности реализации
Полное удаление аккаунта и транспортных данных из системы невозможно (при удалении устанавливается флаг isDeleted на True). С другой стороны, информацию об аренде можно полностью удалить. Это сделано с целью сохранения истории аренды, предотвращая возможную потерю данных.

Для хранения данных об аккаунтах, транспорте и арендах используется PostgreSQL. Модели данных находятся в папке [models](https://github.com/mrgick/volga-it-2023/tree/main/src/models).

Система использует Redis для хранения заблокированных JWT-токенов в течение 31 дня (выдается JWT-токен на 30 дней при авторизации, метод /api/Account/SignOut). Также Redis хранит информацию об удаленных аккаунтах в течение 31 дня, чтобы дать достаточно времени для истечения срока действия токена JWT.

Логика проверки JWT реализована в [tools/jwt.py](https://github.com/mrgick/volga-it-2023/blob/main/src/tools/jwt.py)

В некоторых частях системы добавлена дополнительная логика, например, предотвращение входа в удаленный аккаунт. Детали логики описаны в Swagger для соответствующих методов.

В методе /api/Rent/New/{transportId} реализована дополнительная проверка: баланс пользователя должен содержать сумму, достаточную для оплаты как минимум 2 дней аренды при посуточной аренде или 1 дня при поминутной аренде.

## Структура сервиса
```
src
├── main.py - основной файл
├── config.py - настройки (подтягиваются из .env) 
├── database.py - подключение к PostgreSQL и к Redis
├── models - модели базы данных
├── routers - описание доступных HTTP-методов
├── schemas - схемы запросов, что приходит и что выходит
├── services - логика работы (вызывается роутерами)
└── tools - дополнительные средства (ошибки, jwt и т.д.)
```


## Как запустить сервис локально
1. Скачать с github репозиторий
```bash
git clone https://github.com/mrgick/volga-it-2023.git
```
2. Скопировать .env_example в .env
```bash
cp .env_example .env
```
3. Запустить сервис

    1. используя docker

        1. Windows - скачать и установить [Docker Desktop](https://www.docker.com/products/docker-desktop/), собрать и запустить docker-compose.yaml
        2. Linux/MacOS
        ```bash
        docker-compose up
        ```

    2. вручную

        1. Нужно скачать и установить: [Python 3.11](https://www.python.org/downloads/), [PostgreSQL 15.4](https://www.postgresql.org/download/), [Redis 7.2](https://redis.io/docs/getting-started/installation/)
        2. Создать виртуальную среду python
        ```bash
        python -m venv venv
        ```
        3. Активировать среду python
           1. Windows
           ```bash
           source venv/scripts/activate
           ```
           2. Linux/MacOS
           ```bash
           . venv/bin/activate
           ```
        4. Установить зависимости
        ```bash
        pip install -r requirements.txt
        ```
        5. Создать новую базу данных (db_name)
        6. Исправить доступ к PostgreSQL и к Redis в .env

            Пример:
        ```bash
        DATABASE_URL=postgresql+asyncpg://postgres:@localhost:5432/db_name
        REDIS_URL=redis://localhost:6379
        ```
        7. Запустить сервер
        ```bash
        uvicorn src.main:app --host 127.0.0.1 --port 8000
        ```
4. Swagger будет доступен по адресу http://127.0.0.1:8000/docs#/

> При запуске сервера автоматически инициализируется база данных PostgreSQL (если соответствующие таблицы ещё не существуют) и создается учетная запись "admin" с паролем "admin". Этот пользователь имеет статус администратора и создан для упрощения ручного тестирования.
