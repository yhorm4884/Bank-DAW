shell: 
	python manage.py shell

makemigrations blog:
	python manage.py makemigrations {{ blog }}


migrate:
	python manage.py migrate

runserver:
	python manage.py runserver

startapp app:
    python manage.py startapp {{ app }}

create site:
	python -m venv .venv --promt {{ site }}

superuser:
	python manage.py createsuperuser

createproject project:
	django-admin startproject {{ project }} .