# Installation
The installation steps are as follows (the Docker file needs fixing; it is not working yet).
## Prerequisites
- python 3.12
- django 4.2
- PostgreSQL
- redis 8
<br>
Note : All prerequisites will be installed during the installation process.

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
python webapp/manage.py makemigrations
```
```
python webapp/manage.py migrate
```
```
python webapp/manage.py create_groups
```
```
python webapp/manage.py runserver
```