shell: 
	python3 manage.py shell

makemigrations blog:
	python3 manage.py makemigrations {{ blog }}

migrate:
	python3 manage.py migrate

run:
	python3 manage.py runserver

startapp app:
    python3 manage.py startapp {{ app }}

create site:
	python3 -m venv .venv --promt {{ site }}

superuser:
	python3 manage.py createsuperuser

createproject project:
	django-admin startproject {{ project }} .
	
check:
	python manage.py check
	clean:
    find . -name '*.pyc' -exec rm {} \;

makemigrations app="": _database
    python manage.py makemigrations {{ app }}