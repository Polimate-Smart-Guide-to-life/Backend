#!/usr/bin/env bash
set -euo pipefail

BOLD='\033[1m'
DIM='\033[2m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

banner() {
    local msg="$1"
    echo
    printf "${BOLD}${BLUE}%s${NC}\n" "============================================================"
    printf "${BOLD}%s${NC}\n" "$msg"
    printf "${BOLD}${BLUE}%s${NC}\n" "============================================================"
}

section() {
    local msg="$1"
    echo
    printf "${BOLD}${CYAN}» %s${NC}\n" "$msg"
}

ok() { printf "${GREEN}✓ %s${NC}\n" "$1"; }
warn() { printf "${YELLOW}⚠ %s${NC}\n" "$1"; }
fail() { printf "${RED}✗ %s${NC}\n" "$1"; }

PROJECT_NAME="polimate_test"
DOCKER_COMPOSE_FILE="docker/dev.docker-compose.test.yml"

SUMMARY_LINES=()

cleanup() {
    section "Cleaning up containers, networks, and volumes"
    docker compose -p "$PROJECT_NAME" -f "$DOCKER_COMPOSE_FILE" down -v --remove-orphans >/dev/null 2>&1 || true
}

trap cleanup EXIT

banner "PoliMate Backend Test Runner"

if [ ! -f "$DOCKER_COMPOSE_FILE" ]; then
        fail "Error: File $DOCKER_COMPOSE_FILE not found"
    exit 1
fi

section "Resetting previous test stack (if any)"
docker compose -p "$PROJECT_NAME" -f "$DOCKER_COMPOSE_FILE" down -v --remove-orphans >/dev/null 2>&1 || true

section "Starting fresh test stack"
docker compose -p "$PROJECT_NAME" -f "$DOCKER_COMPOSE_FILE" up --build -d

section "Waiting for database to be ready"
DB_CONTAINER=$(docker compose -p "$PROJECT_NAME" -f "$DOCKER_COMPOSE_FILE" ps -q db_test)
if [ -z "$DB_CONTAINER" ]; then
        fail "Database container 'db_test' not found"
    exit 1
fi

until docker exec "$DB_CONTAINER" pg_isready -U postgres > /dev/null 2>&1; do
  sleep 1
done
ok "Database is healthy"

WEB_CONTAINER=$(docker compose -p "$PROJECT_NAME" -f "$DOCKER_COMPOSE_FILE" ps -q web_test)
if [ -z "$WEB_CONTAINER" ]; then
        fail "Web container 'web_test' not found"
    exit 1
fi

STATUS=$(docker inspect --format '{{.State.Status}}' "$WEB_CONTAINER")
if [ "$STATUS" != "running" ]; then
        fail "Web container is not running (status: $STATUS)"
    exit 1
fi

run_module() {
    local idx="$1"; shift
    local name="$1"; shift
    local path="$1"; shift
    section "Running tests (${idx}/3): ${name}"
    local start_ts end_ts elapsed status
    start_ts=$(date +%s)
    if docker exec "$WEB_CONTAINER" python -W ignore manage.py test "$path" --settings=api.settings; then
        status="${GREEN}PASS${NC}"
    else
        status="${RED}FAIL${NC}"
    fi
    end_ts=$(date +%s)
    elapsed=$(( end_ts - start_ts ))
    SUMMARY_LINES+=("${name} | ${status} | ${elapsed}s")
    if [[ "$status" == *FAIL* ]]; then
        fail "${name} tests failed (${elapsed}s). See logs above."
        exit 1
    fi
}

run_module 1 "users" "apps/users/tests"
run_module 2 "help & support" "apps/questions/tests"
run_module 3 "LLM" "apps/llm/tests"

banner "Test Results"
echo
ok "All modules completed successfully"