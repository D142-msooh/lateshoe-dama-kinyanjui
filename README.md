# Late Show API

A Flask REST API for managing episodes, guests, and their appearances on a late-night talk show.

## Description

This API allows you to manage episodes of a late-night show, guests who appear on the show, and track their appearances with ratings. The application demonstrates a many-to-many relationship between Episodes and Guests through an Appearances join table.

## Features

- View all episodes and guests
- View individual episode details with appearances
- Create new appearances with ratings
- Automatic cascade deletion for related appearances
- Input validation for ratings (1-5 scale)

## Technologies Used

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd lateshoe-dama-kinyanjui
```

2. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install flask flask-sqlalchemy flask-migrate sqlalchemy-serializer
```

4. Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. Seed the database:
```bash
python seed.py
```

6. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5555`

## Database Schema

### Episode
- `id`: Integer (Primary Key)
- `date`: String
- `number`: Integer

### Guest
- `id`: Integer (Primary Key)
- `name`: String
- `occupation`: String

### Appearance
- `id`: Integer (Primary Key)
- `rating`: Integer (1-5, validated)
- `episode_id`: Foreign Key → episodes.id
- `guest_id`: Foreign Key → guests.id

## API Endpoints

### GET /episodes
Returns a list of all episodes.

**Response:**
```json
[
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1
  },
  {
    "id": 2,
    "date": "1/12/99",
    "number": 2
  }
]
```

### GET /episodes/:id
Returns details of a specific episode including all appearances.

**Success Response:**
```json
{
  "id": 1,
  "date": "1/11/99",
  "number": 1,
  "appearances": [
    {
      "episode_id": 1,
      "guest": {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
      },
      "guest_id": 1,
      "id": 1,
      "rating": 4
    }
  ]
}
```

**Error Response (404):**
```json
{
  "error": "Episode not found"
}
```

### GET /guests
Returns a list of all guests.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Michael J. Fox",
    "occupation": "actor"
  },
  {
    "id": 2,
    "name": "Sandra Bernhard",
    "occupation": "Comedian"
  }
]
```

### POST /appearances
Creates a new appearance linking a guest to an episode.

**Request Body:**
```json
{
  "rating": 5,
  "episode_id": 2,
  "guest_id": 3
}
```

**Success Response (201):**
```json
{
  "id": 162,
  "rating": 5,
  "guest_id": 3,
  "episode_id": 2,
  "episode": {
    "date": "1/12/99",
    "id": 2,
    "number": 2
  },
  "guest": {
    "id": 3,
    "name": "Tracey Ullman",
    "occupation": "television actress"
  }
}
```

**Error Response (400):**
```json
{
  "errors": ["validation errors"]
}
```

## Validations

- **Appearance rating**: Must be between 1 and 5 (inclusive)

## Testing

You can test the API using the provided Postman collection:
1. Import `challenge-4-lateshow.postman_collection.json` into Postman
2. Run the requests to verify all endpoints work correctly

## Author

Dama Kinyanjui

## License

This project is licensed under the MIT License.
