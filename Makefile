POSTGRES_CONTAINER_NAME=mlm-bot-postgres
WEB_CONTAINER_NAME=mlm-bot-web
WEB_SERVICE_NAME=web
DEFAULT_DB=postgres


all:
	n=$(n); while [ $${n} -gt 0 ] ; do echo $$n ; n=`expr $$n - 1`; done; true

mkm:
	docker exec -it ${WEB_CONTAINER_NAME} python manage.py makemigrations


m:
	docker exec -it ${WEB_CONTAINER_NAME} python manage.py migrate


csu:
	docker exec -it ${WEB_CONTAINER_NAME} python manage.py createsuperuser


schema:
	docker exec -it ${WEB_CONTAINER_NAME} python manage.py generateschema > openapi-schema.yml


bash:
	docker exec -it ${WEB_CONTAINER_NAME} bash

cs:
	docker exec -it ${WEB_CONTAINER_NAME} python manage.py collectstatic

build:
	docker-compose build


rm_m:
	docker exec -it ${WEB_CONTAINER_NAME} find /code/apps/ -path "*/migrations/*" -not -name "__init__.py" -delete
	docker exec -it ${WEB_CONTAINER_NAME} find /code/core/ -path "*/migrations/*" -not -name "__init__.py" -delete

rn:
	docker-compose down
	docker-compose build
	docker-compose up -d web
	make rm_m
	make mkm
	make m
	make csu
	docker-compose stop

gen_cert:
	docker exec -it ${WEB_CONTAINER_NAME} python -c "from generate_app.cloudflare import generate_certificate; from core.models import App; generate_certificate(App.objects.all())"

log_nginx:
	docker exec -it ${WEB_CONTAINER_NAME} tail -f /var/log/nginx/*
