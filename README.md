# Foodgram
https://www.eda-project.tk/recipe/

Проект foodgram позволяет полььзователям постить рецепты с картинками, добавлять понравившиеся рецепты в избранное, подписываться на любимых атворов и создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

# Технические требования для развертывания проекта
Python3.8 и выше, Docker, Docker-Compose

# Инструкция по развертыванию проекта
1. Скачать проект или клонировать с помощью git 
```
git clone https://github.com/Caterina-Plewako/foodgram-project.git
```

2. Перейти в каталог с проектом и создать виртуальное окружение 
```
python -m venv venv
```

3. Запустить виртуальное окружение:

Для Mac/Linux:
```
source venv/bin/activate
```

Для Windows:
```
source venv/Scripts/activate
```

4. Установить все необходимые пакеты, указанные в файле requirements.txt 
```
pip install -r requirements.txt
```

5. Запустить миграции 
```
python manage.py migrate
```

6. Для проверки работы проекта запустить тестовый сервер 
```
python manage.py runserver
```

7. Перейти по адресу http://127.0.0.1:8000

# Для работы с админкой Django:
1. Создать суперпользователя 
```
python manage.py createsuperuser
```
2. Перейти по адресу http://127.0.0.1:8000/admin и ввести логин и пароль суперпользователя

# Технологии 
* Python
* Django
* PostgreSQL
* Docker
* Docker-compose
