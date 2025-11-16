# How to run the Backend Server

### Step 1 - Docker
You need to have docker installed in your PC.

### Step 2 - Build
Run in the terminal:
``` bash
make build
```

### Step 3 - Makemigrations and run them
1. Create migrations
``` bash
make makemigrations
```

2. Run migrations
``` bash
make migrate
```

### Step 4 - Run server
``` bash
make runserver
```

________________________________________________________________________________________

# Make and run migrations

### Step 1
Create or add modifications to the model in the folder `model` of the app.

### Step 2 - Create migrations
Run in the terminal:
``` bash
make makemigrations
```
This should create a file in the folder `migrations` of your app.

### Step 3 - Run migrations
Run:
``` bash
make migrate
```

________________________________________________________________________________________

# Create the admin user
Run in the terminal:
``` bash
make createsuperuser
```

________________________________________________________________________________________

# Tests

Use the test runner script to execute all tests in a clean, isolated Docker Compose project. It runs each module in order and cleans up containers, networks, and volumes afterward.

```bash
make runtests
```

What this does:
- Brings up a fresh test stack using a dedicated compose project name (avoids clashes with dev containers/volumes)
- Waits for Postgres to be healthy
- Runs tests in deterministic order
- Shuts everything down with full cleanup (`--remove-orphans -v`)

All test files print clear terminal banners, per-test PASS messages, and a final timing summary for easy reading.

## Test cases matrix (by module)

### Users (4 tests)

| No. | Test function | What it checks | Endpoint/Action |
| --- | ------------- | -------------- | --------------- |
| 1 | `test_create_user` | Can register a new user, returns 201 and the created username | POST `users-register` |
| 2 | `test_get_me` | Authenticated “me” endpoint returns correct user details | GET `users-me` |
| 3 | `test_login` | Login returns JWT access and refresh tokens | POST `token_obtain_pair` |
| 4 | `test_update_me` | Partial update updates first_name successfully | PATCH `users-me` |

### Help & Support (2 tests)

| No. | Test function | What it checks | Endpoint/Action |
| --- | ------------- | -------------- | --------------- |
| 1 | `test_create_question` | Can create a new question and it’s attributed to the user | POST `create-question` |
| 2 | `test_get_user_questions` | Fetches the user’s own questions (list, order, content) | GET `user-questions` |

### LLM (6 tests)

| No. | Test function | Scenario | Expected behavior (high-level) | Endpoint |
| --- | ------------- | -------- | ------------------------------ | -------- |
| 1 | `test_confidential_info_refusal` | Attempt to get confidential info | Returns a refusal (no sensitive data) | POST `/llm/conversation/` |
| 2 | `test_normal_university_question` | Normal Polimi-related question | Returns a helpful, step-formatted answer | POST `/llm/conversation/` |
| 3 | `test_follow_up_context_retained` | Follow-up question in same thread | Reply reflects prior context; `message_count` grows | POST `/llm/conversation/` (twice) |
| 4 | `test_off_topic_non_polimi` | Off-topic question | Politely limits scope to Politecnico di Milano | POST `/llm/conversation/` |
| 5 | `test_missing_message_param` | Missing `message` in payload | Returns 400 with `{"error": "message is required"}` | POST `/llm/conversation/` |
| 6 | `test_trending_questions_cached` | Trending FAQs twice | Second call indicates cached data (if Redis available) | GET `/llm/trending-questions/` |
