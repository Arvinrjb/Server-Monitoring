# Installation
The installation steps are as follows 
## Prerequisites
- python 3.12
- django 4.2
- PostgreSQL
- redis 8
<br>
Note : All prerequisites will be installed during the installation process.
Note: Make sure the PostgreSQL and Redis services are running.
## Local Setup
```
git clone https://github.com/Arvinrjb/Server-Monitoring.git
```
```
cd Server-Monitoring
```
```
source .venv-linux/bin/activate
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
<br>
In two separate terminals:
<br>
```
celery -A webapp worker --loglevel=INFO
```
```
celery -A webapp beat --loglevel=INFO
```
```
python manage.py runserver
```