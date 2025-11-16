#!/usr/bin/env bash
set -euo pipefail

DOCKER_COMPOSE_FILE="docker/dev.docker-compose.test.yml"
PROJECT_NAME="polimate_test"

if [ ! -f "$DOCKER_COMPOSE_FILE" ]; then
    echo "Error: File $DOCKER_COMPOSE_FILE not found"
    exit 1
fi

docker compose -p "$PROJECT_NAME" -f "$DOCKER_COMPOSE_FILE" down -v --remove-orphans || true

docker compose -p "$PROJECT_NAME" -f "$DOCKER_COMPOSE_FILE" up --build -d

echo "Waiting for database to be ready..."
DB_CONTAINER=$(docker compose -p "$PROJECT_NAME" -f "$DOCKER_COMPOSE_FILE" ps -q db_test)
if [ -z "$DB_CONTAINER" ]; then
    echo "Error: Database container 'db_test' not found"
    docker compose -p "$PROJECT_NAME" -f "$DOCKER_COMPOSE_FILE" down -v --remove-orphans
    exit 1
fi

until docker exec "$DB_CONTAINER" pg_isready -U postgres > /dev/null 2>&1; do
  sleep 1
done

WEB_CONTAINER=$(docker compose -p "$PROJECT_NAME" -f "$DOCKER_COMPOSE_FILE" ps -q web_test)
if [ -z "$WEB_CONTAINER" ]; then
    echo "Error: Web container 'web_test' not found"
    docker compose -p "$PROJECT_NAME" -f "$DOCKER_COMPOSE_FILE" down -v --remove-orphans
    exit 1
fi

STATUS=$(docker inspect --format '{{.State.Status}}' "$WEB_CONTAINER")
if [ "$STATUS" != "running" ]; then
    echo "Error: Web container is not running (status: $STATUS)"
    docker compose -p "$PROJECT_NAME" -f "$DOCKER_COMPOSE_FILE" down -v --remove-orphans
    exit 1
fi

echo "Running tests (1/3): users"
docker exec "$WEB_CONTAINER" python -W ignore manage.py test apps/users/tests --settings=api.settings

echo "Running tests (2/3): help & support"
docker exec "$WEB_CONTAINER" python -W ignore manage.py test apps/questions/tests --settings=api.settings

echo "Running tests (3/3): LLM"
docker exec "$WEB_CONTAINER" python -W ignore manage.py test apps/llm/tests --settings=api.settings

echo "Cleaning up..."
docker compose -p "$PROJECT_NAME" -f "$DOCKER_COMPOSE_FILE" down -v --remove-orphans