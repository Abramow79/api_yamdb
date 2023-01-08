# A group project of Yandex students.Workshop on the course "API: Program interaction interface"

## Description

The YaMDb project collects user reviews of works.The works are divided into categories: "Categories", "Movies", "Music".The list of categories can be expanded by the administrator (for example, you can add the category "Arthouse").
  
### The works themselves are not stored in YaMDb, you can't watch a movie or listen to music here

In each category there are works: books, movies or music. For example, in the category "Books" there may be works "Winnie the Pooh and everything-everything-everything" and "Martian Chronicles", and in the category "Music" - the song "Just Now" by the group "Insects" and the second suite by Bach.A work can be assigned a genre from the preset list (for example, "Fairy Tale", "Rock" or "Arthouse").Only the administrator can create new genres.
Grateful or outraged users leave text reviews for the works and give the work a rating in the range from one to ten (an integer); an average rating of the work is formed from user ratings — a rating (an integer). The user can leave only one review for one work.

#### Available functionality

- JWT tokens are used for authentication.
- Unauthorized users have read-only access to the API.
- Creation of objects is allowed only to authenticated users.Other functionality is restricted in the form of administrative roles and authorship.
- User management.
- Getting a list of all categories and genres, adding and removing.
- Getting a list of all the works, adding them.Receiving, updating and deleting a specific work.
- Getting a list of all reviews, adding them.Receiving, updating, and deleting a specific review.  
- Getting a list of all comments, adding them.Receiving, updating, and deleting a specific comment.
- The ability to get detailed information about yourself and delete your account.
- Filtering by fields.

#### API documentation is available at [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/) after starting the server with the project

#### Technologies

- Python 3.7
- Django 2.2.16
- Django Rest Framework 3.12.4
- Simple JWT
- SQLite3

## How to launch a project:

Clone the repository and go to it on the command line:
```
git clone https://github.com/Abramow79/api_yamdb
```

Create and activate a virtual environment:
```
python -m venv venv
```
```
source venv/scripts/activate
```

Install dependencies from a file requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python manage.py migrate
```
Launch a project:
```
python manage.py runserver
```

#### Autors

Zheltyakov Mark - [https://github.com/zheltiakov](https://github.com/zheltiakov)
Dmitry Uglov - [https://github.com/pro911pc](https://github.com/pro911pc)   
Andrey Abramov 

## Used technologies
* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Django REST framework](https://www.django-rest-framework.org/)
* [DRF Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

## Useful links

- [DRF Routing](https://www.django-rest-framework.org/api-guide/routers/)
- [DRF Permissions](https://www.django-rest-framework.org/api-guide/permissions/)
- [DRF Filtering and Search](https://www.django-rest-framework.org/api-guide/filtering/)
- [DRF Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [Factory_boy & Django ORM](https://factoryboy.readthedocs.io/en/latest/orms.html#django)
- [Faker: test data generation](https://faker.readthedocs.io/en/master/providers.html)
- [Data migrations](https://docs.djangoproject.com/en/4.1/topics/migrations/)
- [Custom management program](https://docs.djangoproject.com/en/4.1/howto/custom-management-commands/)
- [drf-yasg: OpenAPI Specification generator](https://drf-yasg.readthedocs.io/en/stable/)
- [Django-filters](https://django-filter.readthedocs.io/en/stable/guide/usage.html#declaring-filters)
