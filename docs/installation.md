# Installation
The installation steps are as follows 
## Prerequisites
- python 3.12
- django 4.2
- PostgreSQL
- redis 8
#### Note : All prerequisites will be installed during the installation process.<br>
#### Note: Make sure the PostgreSQL and Redis services are running.

## Local Setup

```
cd Server-Monitoring
```
```
python -m venv .venv
```
```
source .venv/bin/activate
```
```
pip install -r requirements.txt
```
```
cd webapp
```
```
python manage.py makemigrations
```
```
python manage.py migrate
```
```
python manage.py create_groups
```
In two separate terminals:
```
celery -A webapp worker --loglevel=INFO
```
```
celery -A webapp beat --loglevel=INFO
```
```
python manage.py runserver
```

### [Configurations](configurations.md)