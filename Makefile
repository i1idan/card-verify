start:
	docker-compose up
build:
	docker-compose up --build
stop:
	docker-compose down
logs:
	docker-compose logs -f --tail 20