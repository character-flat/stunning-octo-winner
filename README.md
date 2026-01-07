# Notes API with Version History

A FastAPI-based backend for a note-taking application with version history support.

## Features

- **RESTful API** using FastAPI
- **PostgreSQL Database** with SQLAlchemy ORM
- **Version History** - Track all changes to notes
- **Database Migrations** using Alembic
- **Automatic API Documentation** (Swagger UI and ReDoc)

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **PostgreSQL** - Robust relational database
- **SQLAlchemy** - Powerful ORM for database interactions
- **Alembic** - Database migration tool
- **Pydantic** - Data validation using Python type annotations

## Project Structure

```
.
├── alembic/                    # Database migrations
│   ├── versions/              # Migration scripts
│   ├── env.py                 # Alembic environment configuration
│   └── script.py.mako         # Migration template
├── app/                       # Application code
│   ├── models/               # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── note.py           # Note and NoteVersion models
│   ├── routes/               # API endpoints
│   │   ├── __init__.py
│   │   └── notes.py          # Notes CRUD and version endpoints
│   ├── schemas/              # Pydantic schemas
│   │   ├── __init__.py
│   │   └── note.py           # Request/response schemas
│   ├── __init__.py
│   └── database.py           # Database connection and session
├── alembic.ini               # Alembic configuration
├── main.py                   # FastAPI application entry point
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher

### 1. Clone the Repository

```bash
git clone https://github.com/character-flat/stunning-octo-winner.git
cd stunning-octo-winner
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

Create a PostgreSQL database:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE notes_db;

# Exit psql
\q
```

### 5. Configure Environment Variables

Copy the example environment file and update with your database credentials:

```bash
cp .env.example .env
```

Edit `.env` file:
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/notes_db
```

### 6. Run Database Migrations

```bash
alembic upgrade head
```

### 7. Start the Application

```bash
uvicorn main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## API Endpoints

### Notes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/notes/` | Create a new note |
| GET | `/notes/` | List all notes (with pagination) |
| GET | `/notes/{note_id}` | Get a specific note with version history |
| PUT | `/notes/{note_id}` | Update a note (creates new version) |
| DELETE | `/notes/{note_id}` | Delete a note and all its versions |

### Version History

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notes/{note_id}/versions` | Get all versions of a note |
| GET | `/notes/{note_id}/versions/{version_number}` | Get a specific version |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |

## API Usage Examples

### Create a Note

```bash
curl -X POST "http://localhost:8000/notes/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Note",
    "content": "This is the content of my first note."
  }'
```

### Get All Notes

```bash
curl -X GET "http://localhost:8000/notes/"
```

### Get a Specific Note

```bash
curl -X GET "http://localhost:8000/notes/1"
```

### Update a Note

```bash
curl -X PUT "http://localhost:8000/notes/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "content": "Updated content."
  }'
```

### Get Version History

```bash
curl -X GET "http://localhost:8000/notes/1/versions"
```

### Get Specific Version

```bash
curl -X GET "http://localhost:8000/notes/1/versions/1"
```

### Delete a Note

```bash
curl -X DELETE "http://localhost:8000/notes/1"
```

## Database Schema

### Notes Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| title | String(255) | Note title |
| content | Text | Note content |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### Note Versions Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| note_id | Integer | Foreign key to notes table |
| title | String(255) | Version title |
| content | Text | Version content |
| version_number | Integer | Sequential version number |
| created_at | DateTime | Version creation timestamp |

## Version History Feature

The version history feature automatically creates a snapshot of the note whenever:
1. A note is created (version 1)
2. A note is updated (incremental version numbers)

Each version preserves the title and content at that point in time, allowing users to:
- View all historical versions of a note
- Retrieve specific versions
- Track changes over time

## Development

### Creating New Migrations

When you modify database models, create a new migration:

```bash
alembic revision --autogenerate -m "description of changes"
```

Then apply the migration:

```bash
alembic upgrade head
```

### Running with Different Database

Update the `DATABASE_URL` in your `.env` file or set it as an environment variable:

```bash
export DATABASE_URL="postgresql://user:password@host:port/dbname"
```

## Testing the API

You can test the API using:
1. **Swagger UI**: Navigate to http://localhost:8000/docs
2. **ReDoc**: Navigate to http://localhost:8000/redoc
3. **curl**: Use the examples provided above
4. **Postman** or any other API client

## License

MIT