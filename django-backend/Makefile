build:
	docker build -t x-pictures-backend:latest -f docker/Dockerfile .

up:
	docker-compose -f docker/docker-compose.yaml up -d --build

down:
	docker-compose -f docker/docker-compose.yaml down

stop:
	docker-compose -f docker/docker-compose.yaml stop

restart:
	docker-compose -f docker/docker-compose.yaml down && docker-compose -f docker/docker-compose.yaml up -d --build

makemigrations:
	docker exec -it x-pictures-backend bash -c 'python manage.py makemigrations'

migrate:
	docker exec -it x-pictures-backend bash -c 'python manage.py migrate'

enter:
	docker exec -it x-pictures-backend bash

search-rebuild:
	docker exec -it x-pictures-backend bash -c 'python manage.py search_index --rebuild'
