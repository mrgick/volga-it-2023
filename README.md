# Simbir.GO API
Волга IT - Задание полуфинального этапа дисциплины Backend-разработка: Web API.

Проект реализован на python 3.11 с использованием PostgreSQL и Redis.

Задание лежит в файле [task.pdf](https://github.com/mrgick/volga-it-2023/blob/main/task.pdf)

## Особенности реализации
TODO: дописать

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

        1. Windows - скачать и установить [Docker Desktop](https://www.docker.com/products/docker-desktop/)
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
           1. Windows/MacOS
           ```bash
           source venv/scripts/activate
           ```
           2. Linux
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

P.S. При запуске сервера инициализируется база данных в PostgreSQL (если таблиц ещё не существует) и создастся пользователь "admin" с паролем "admin" - администратор (если его еще не существует) - реализовано для облегчения ручного тестирования.

