# HEALTH CARE FRAUD PROJECT

## Как запустить проект:
- Установите Docker, инструкция:
https://docs.docker.com/get-docker/

- Установите docker-compose, инструкция:
https://docs.docker.com/compose/install/

- Клонируйте репозиторий:
```
git clone git@github.com:ilyarogozin/googlesheets.git
```

- Соберите контейнеры и запустите их:
```
docker-compose up -d --build
```

- Выполните миграции:
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

- Запустите проект:
```
docker-compose exec web python manage.py runserver
```

## Примеры запросов:

