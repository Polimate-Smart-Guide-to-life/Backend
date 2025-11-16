build:
	docker compose -f docker/dev.docker-compose.yml build

makemigrations:
	docker compose -f docker/dev.docker-compose.yml up -d
	docker compose -f docker/dev.docker-compose.yml exec web python3 manage.py makemigrations
	docker compose -f docker/dev.docker-compose.yml down

migrate:
	docker compose -f docker/dev.docker-compose.yml up -d
	docker compose -f docker/dev.docker-compose.yml exec web python3 manage.py migrate
	docker compose -f docker/dev.docker-compose.yml down

runserver:
	docker compose -f docker/dev.docker-compose.yml up

up:
	docker compose -f docker/dev.docker-compose.yml up -d

down:
	docker compose -f docker/dev.docker-compose.yml down

shell:
	docker compose -f docker/dev.docker-compose.yml up -d
	docker compose -f docker/dev.docker-compose.yml exec web python3 manage.py shell
	docker compose -f docker/dev.docker-compose.yml down

createsuperuser:
	docker compose -f docker/dev.docker-compose.yml up -d
	docker compose -f docker/dev.docker-compose.yml exec web python3 manage.py createsuperuser
	docker compose -f docker/dev.docker-compose.yml down

runtests:
	chmod +x ./run_tests.sh
	./run_tests.sh
