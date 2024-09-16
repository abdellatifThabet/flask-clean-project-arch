build:
	@docker-compose build

# this is run only one time to generate the migrations folder
db-init:
	@docker-compose run python-api flask db init

db-upgrade:
	@docker-compose up -d db
	@sleep 5
	@docker-compose run python-api flask db upgrade --directory migrations

stop:
	@docker-compose down --remove-orphans
	@docker-compose -f docker-compose-test.yaml down --remove-orphans

db-migrate: build
	@docker-compose run python-api flask db migrate --directory migrations

run: stop build db-upgrade
	@docker-compose up  --remove-orphans

# for unit tests
test-build:
	@docker-compose -f docker-compose-test.yaml build

test-db-upgrade:
	@docker-compose -f docker-compose-test.yaml up -d db-test
	@sleep 5
	@docker-compose -f docker-compose-test.yaml run api-test flask db upgrade --directory migrations

test: stop test-build test-db-upgrade
	@docker-compose -f docker-compose-test.yaml run api-test pytest -vv tests