# HEALTH CARE FRAUD PROJECT

## Как запустить проект:

- Клонируйте репозиторий:
```
git clone git@github.com:ilyarogozin/health_care_fraud_project.git
```
---
- Создайте окружение и установите зависимости:
```
python3 -m venv venv && pip install -r requirements.txt
```
---
- Зайдите в папку с файлом manage.py:
```
cd medical_services
```
---
- Выполните миграции:
```
python3 manage.py makemigrations && python3 manage.py migrate
```
---
- Запустите проект:
```
python3 manage.py runserver
```

## Примеры запросов:
- POST с файлом client_org.xlsx
```
http://localhost:8000/api/upload_client_org/
```
---
- POST с файлом bills.xlsx
```
http://localhost:8000/api/upload_bills/
```
---
- GET для получения списка клиентов
```
http://localhost:8000/api/get_clients_list/
```
---
- GET для получения списка чеков
```
http://localhost:8000/api/get_bills_list/
```
---
- GET для получения списка чеков с фильтрацией по имени клиента или названию организации(фильтрация производится по содержанию, а не точному совпадению и не чувствительна к регистру)
```
http://localhost:8000/api/get_bills_list?client_org=client2org1
```
```
http://localhost:8000/api/get_bills_list?client_name=client2
```
---
#### PS: все запросы тестировал через Postman(всё работает), файлы загружал через form-data