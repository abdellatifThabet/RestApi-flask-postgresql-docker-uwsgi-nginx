build:
	@docker-compose build

db-upgrade:
	@docker-compose up -d db
	@sleep 5
	@docker-compose run python-api flask db upgrade --directory migrations

stop:
	@docker-compose down --remove-orphans

db-migrate: build
	@docker-compose run python-api flask db migrate --directory migrations

run: stop build db-upgrade
	@docker-compose up  --remove-orphans

