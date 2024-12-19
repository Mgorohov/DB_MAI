DC = docker compose
EXEC = docker exec -it
DB_CONTAINER = example-db
LOGS = docker logs
ENV_FILE = --env-file .env
APP_FILE = docker-compose.yaml
APP_CONTAINER = main-app
MANAGEPY = python manage.py

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV_FILE} up --build -d


.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f


.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down