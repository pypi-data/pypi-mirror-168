# MP-Reviews

Django reviews app.

### Installation

Install with pip:

```sh
$ pip install django-mp-reviews
```

Add reviews to settings.py:

```
INSTALLED_APPS = [
    'reviews',
]
```

Add reviews to urls.py:
```
urlpatterns = [
    path('reviews/', include('reviews.urls'))
]
```

Add bower components:
```
BOWER_INSTALLED_APPS = (
	'jquery#1.11.1',
	'jquery-form',
	'jquery.rateit',
)
```

Install bower components:

```
$ python manage.py bower install
```

Run migrations:

```
$ python manage.py migrate
```

### Requirements

App require this packages:

* django-mp-pagination
