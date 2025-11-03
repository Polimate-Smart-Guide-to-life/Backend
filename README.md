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


## Maps API

The maps app manages locations, campuses, buildings, and rooms inside the project.

### Available Endpoints

| Method | Endpoint | Description |
|---------|-----------|--------------|
| `GET` | `/api/maps/<slug>/` | Returns a full campus (with all its buildings and rooms). |
| `GET` | `/api/buildings/<id>/` | Returns details of a single building and its rooms. |
| `GET` | `/api/rooms/<id>/` | Returns information about a specific room. |

### Example
`GET /api/maps/leonardo-32/`

```json
{
  "id": 1,
  "name": "Leonardo 32",
  "slug": "leonardo-32",
  "buildings": [
    {
      "id": 13,
      "name": "Building 13",
      "rooms": [
        {"id": 101, "name": "Room 13.1"},
        {"id": 102, "name": "Room 13.2"}
      ]
    }
  ]
}