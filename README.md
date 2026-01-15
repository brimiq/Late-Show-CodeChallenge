# Late Show API

A Flask REST API for managing episodes, guests, and guest appearances on a late-night talk show.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing with Postman](#testing-with-postman)
- [Models](#models)
- [Validations](#validations)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This API provides endpoints to manage a late-night talk show database, including:

- **Episodes**: View all episodes or get details of a specific episode
- **Guests**: View all guests who appeared on the show
- **Appearances**: Create new guest appearances and view existing ones

The API follows RESTful principles and returns JSON responses.

---

## Features

- ✅ RESTful API design
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Database migrations with Flask-Migrate
- ✅ Cascade delete for data integrity
- ✅ Input validation for ratings
- ✅ Seed data generation from CSV
- ✅ Comprehensive error handling
- ✅ Well-documented endpoints

---

## Project Structure

```
late-show/
├── app.py                    # Main Flask application entry point
├── config.py                 # Configuration settings
├── models.py                 # Database models (Episode, Guest, Appearance)
├── routes.py                 # API route definitions
├── seed.py                   # Database seeding script
├── requirements.txt          # Python dependencies
├── migrations/               # Flask-Migrate migration files
├── instance/                 # SQLite database storage
├── data/                     # Data files directory
│   └── guest_data.csv       # CSV file for guest data (optional)
└── README.md                 # This file
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd late-show
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create the instance directory**:
   ```bash
   mkdir instance
   ```

---

## Configuration

The application uses a `config.py` file for configuration. The default settings use SQLite for development:

```python
# config.py
SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/late_show.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'your-secret-key-change-in-production'
```

### Changing the Database

To use PostgreSQL or another database, update the `SQLALCHEMY_DATABASE_URI`:

```python
# PostgreSQL example
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/late_show'
```

---

## Database Setup

### 1. Initialize Migrations

Run the following command to initialize Flask-Migrate:

```bash
flask --app app db init
```

### 2. Create Migration

Generate the initial migration:

```bash
flask --app app db migrate -m "Initial migration"
```

### 3. Apply Migrations

Apply the migration to create the database schema:

```bash
flask --app app db upgrade
```

### 4. Seed the Database

Populate the database with sample data:

```bash
python seed.py
```

**Note**: If you have a `guest_data.csv` file in the `data/` directory, the seed script will use it. Otherwise, it will use sample data.

---

## Running the Application

### Development Mode

Run the Flask development server:

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Using Flask CLI

Alternatively, you can use the Flask CLI:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

---

## API Endpoints

### Base URL

```
http://localhost:5000
```

### Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/episodes` | Get all episodes |
| GET | `/episodes/<id>` | Get a specific episode with appearances |
| GET | `/guests` | Get all guests |
| POST | `/appearances` | Create a new appearance |

---

### GET /episodes

Get a list of all episodes.

**URL**: `GET /episodes`

**Response** (200 OK):
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

---

### GET /episodes/:id

Get details of a specific episode, including all appearances.

**URL**: `GET /episodes/<id>`

**Parameters**:
- `id` (integer): The episode ID

**Response** (200 OK):
```json
{
  "id": 1,
  "date": "1/11/99",
  "number": 1,
  "appearances": [
    {
      "id": 1,
      "rating": 4,
      "guest_id": 1,
      "episode_id": 1,
      "guest": {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
      }
    }
  ]
}
```

**Response** (404 Not Found):
```json
{
  "error": "Episode not found"
}
```

---

### GET /guests

Get a list of all guests.

**URL**: `GET /guests`

**Response** (200 OK):
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

---

### POST /appearances

Create a new guest appearance on an episode.

**URL**: `POST /appearances`

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "rating": 5,
  "episode_id": 1,
  "guest_id": 2
}
```

**Response** (201 Created):
```json
{
  "id": 162,
  "rating": 5,
  "guest_id": 2,
  "episode_id": 1,
  "episode": {
    "date": "1/11/99",
    "id": 1,
    "number": 1
  },
  "guest": {
    "id": 2,
    "name": "Sandra Bernhard",
    "occupation": "Comedian"
  }
}
```

**Response** (400 Bad Request):
```json
{
  "errors": [
    "Rating must be between 1 and 5 (inclusive)",
    "Guest not found"
  ]
}
```

---

## Testing with Postman

### Import Postman Collection

1. Download the Postman collection: `challenge-4-lateshow.postman_collection.json`
2. Open Postman
3. Click "Import" and select the JSON file
4. The collection will be imported with all test requests

### Testing Steps

1. Start the Flask server: `python app.py`
2. Import the Postman collection
3. Run the requests in the following order:
   - `GET /episodes` - Verify you get the episode list
   - `GET /episodes/:id` - Verify episode detail with appearances
   - `GET /guests` - Verify guest list
   - `POST /appearances` - Test creating a new appearance

---

## Models

### Episode

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| date | String | Air date (e.g., "1/11/99") |
| number | Integer | Episode number |

**Relationships**:
- Has many `Appearance` objects (cascade delete enabled)

### Guest

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | Guest name |
| occupation | String | Guest occupation |

**Relationships**:
- Has many `Appearance` objects (cascade delete enabled)

### Appearance

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| rating | Integer | Rating (1-5) |
| guest_id | Integer | Foreign key to Guest |
| episode_id | Integer | Foreign key to Episode |

**Relationships**:
- Belongs to `Guest`
- Belongs to `Episode`

---

## Validations

### Appearance Rating

The `rating` field for appearances must be between 1 and 5 (inclusive):

- ✅ Valid: 1, 2, 3, 4, 5
- ❌ Invalid: 0, 6, -1, 10

If validation fails, the API returns:
```json
{
  "errors": ["Rating must be between 1 and 5 (inclusive)"]
}
```

### Required Fields

For POST `/appearances`:
- `rating` (required)
- `episode_id` (required, must exist)
- `guest_id` (required, must exist)

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a Pull Request

---

## License

This project is for educational purposes as part of a coding challenge.

---

## Support

For questions or issues, please open a GitHub issue in the repository.

