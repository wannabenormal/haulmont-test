# Haulmont test task

## Installation
1. Copy this repository to your local machine.
2. Create a [virtual environment](https://docs.python.org/3/library/venv.html).
3. Install requirements with pip:
```
pip install -r requirements.txt
```
4. Create a superuser with:
```
python manage.py create superuser
```
5. Run local server:
```
python manage.py runserver
```

## Usage
This project use [DRF](https://www.django-rest-framework.org/) to access API endpoints.
All endpoints are starts with `/api` prefix.
All endpoints can be viewed in `/notes/urls.py`.

This project use DRF Browsable Api, so you can fetch data with your browser by accessing endpoints urls directly.