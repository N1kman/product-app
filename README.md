## Content

[About](#about)

[Schema](#shema)

[Local start](#local-start)

[Alembic](#alembic)

[Docker](#docker)

## About

This is a fastapi application that can provide API in various languages.
The application is developed based on asynchronous sqlalchemy, alembic, kafka.
The mbart model was used for translation.
The application can also be deployed in Docker.

## Schema

![Описание изображения](docs/schema.jfif)

## Local start

To run the application you will need Postgresql.
You will also need to install kafka, a detailed post about this <a href="https://timeweb.cloud/tutorials/microservices/ustanovka-i-nastroika-kafka">here</a>.
Next, enter the following commands in terminal:
```
cd ./app
pip install -r requirements.txt
```
This will download all dependencies.
To run in HTTPS mode, use the api environment variable in the <a href="_envs/.env-api">_envs folder</a>.

## Alembic

Alembic is configured specifically so you only need to update:
```
alembic upgrade head
```

## Docker

Use only 1 command:
```
docker compose up --build
```

To use https, you need to uncomment the line with the ssl parameters, and comment out the other one in the <a href="Dockerfile">dockerfile</a>.
