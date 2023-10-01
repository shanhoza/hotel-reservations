# Бронирование отелей
Репозиторий является серверной частью бэкенд приложения. Полное приложение запущено по ссылке: **временно отсутствует** 

# Эндпоинты приложения
* Эндпоинт авторизации 
* Эндпоинт регистрации
* Эндпоинт с админкой
* Эндпоинты CRUD'a бронирований
* Эндпоинт получения отелей и его номеров
* Эндпоинт загрузки фотографий отелей

# Основной стек технологий 
* Python
    * FastAPI
    * pytest + httpx
* PostgreSQL
* SQLAlchemy
  * alembic
* Celery
  * Redis
  * Flower
* SQLAdmin
* Docker
* Docker-compose
* Sentry
* Prometheus
* Grafana

## Запуск проекта
### 0. Для запуска всего проекта 
Для запуска всех сервисов (БД, Redis, веб-сервер (FastAPI), Celery, Flower, Grafana, Prometheus) необходимо использовать файл docker-compose.yml и команды
```
docker-compose up --build
```
После запуска Swagger/OpenAPI документация будет доступна по адресу http://localhost:7777/v1/docs#/

#### 1. Запуск приложения
Для запуска FastAPI используется веб-сервер uvicorn. Команда для запуска выглядит так:  
```
python app/main.py
```  
Ее необходимо запускать в командной строке, обязательно находясь в корневой директории проекта.

#### 2. Celery & Flower
Для запуска Celery используется команда  
```
celery -A app.tasks.celery:celery worker --loglevel=INFO
```
Для запуска Flower используется команда  
```
celery -A app.tasks.celery:celery flower
``` 

#### 3. Dockerfile
Для запуска веб-сервера (FastAPI) внутри контейнера необходимо раскомментировать код внутри Dockerfile и иметь уже запущенный экземпляр PostgreSQL на компьютере.
Код для запуска Dockerfile:  
```
docker build .
```  
Команда также запускается из корневой директории, в которой лежит файл Dockerfile.
