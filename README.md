# Notes API with Version History

A FastAPI-based backend for a note-taking application with version history.

## Features

- **User Authentication**: Register and login with JWT tokens
- **Notes Management**: Full CRUD operations for notes
- **Version History**: Automatic version tracking on note updates
- **Version Restore**: Restore notes to any previous version
- **PostgreSQL Database**: Robust data storage with SQLAlchemy ORM
- **Alembic Migrations**: Database schema versioning
- **Pydantic Validation**: Request/response schema validation
- **Comprehensive Tests**: Pytest-based test suite
- **Postman Collection**: Ready-to-use API documentation

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Validation**: Pydantic
- **Testing**: pytest

## Project Structure

```
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── auth.py      # Authentication endpoints
│   │   │   ├── notes.py     # Notes CRUD & version endpoints
│   │   │   └── users.py     # User endpoints
│   │   ├── deps.py          # Dependencies (auth, db)
│   │   └── router.py        # API router
│   ├── core/
│   │   ├── config.py        # Application settings
│   │   └── security.py      # JWT & password utilities
│   ├── db/
│   │   └── database.py      # Database connection
│   ├── models/
│   │   ├── user.py          # User model
│   │   └── note.py          # Note & NoteVersion models
│   ├── schemas/
│   │   ├── user.py          # User Pydantic schemas
│   │   └── note.py          # Note Pydantic schemas
│   ├── tests/
│   │   ├── conftest.py      # Test fixtures
│   │   ├── test_auth.py     # Authentication tests
│   │   ├── test_notes.py    # Notes CRUD tests
│   │   └── test_versions.py # Version history tests
│   └── main.py              # FastAPI application
├── alembic/
│   ├── versions/            # Migration scripts
│   └── env.py               # Alembic environment
├── postman/
│   └── Notes_API_Collection.json  # Postman collection
├── alembic.ini              # Alembic configuration
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── pytest.ini               # Pytest configuration
```

## Local Development Setup

### Prerequisites

- Python 3.10+
- PostgreSQL 13+

### 1. Clone the Repository

```bash
git clone <repository-url>
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

### 4. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

**Required Environment Variables:**

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@localhost:5432/notes_db` |
| `SECRET_KEY` | JWT signing key (change in production!) | `your-secret-key-change-in-production` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |

### 5. Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE notes_db;
```

### 6. Run Migrations

```bash
alembic upgrade head
```

### 7. Start the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 8. Access Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest app/tests/test_auth.py

# Run with coverage
pip install pytest-cov
pytest --cov=app
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Login (OAuth2 form) |
| POST | `/api/v1/auth/login/json` | Login (JSON body) |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/users/me` | Get current user info |

### Notes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/notes/` | Create a note |
| GET | `/api/v1/notes/` | Get all user's notes |
| GET | `/api/v1/notes/{note_id}` | Get a specific note |
| PUT | `/api/v1/notes/{note_id}` | Update a note |
| DELETE | `/api/v1/notes/{note_id}` | Delete a note |

### Version History

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/notes/{note_id}/versions` | Get all versions of a note |
| GET | `/api/v1/notes/{note_id}/versions/{version_number}` | Get specific version |
| POST | `/api/v1/notes/{note_id}/restore` | Restore to previous version |

## Postman Collection

Import the Postman collection from `postman/Notes_API_Collection.json` to test all endpoints.

The collection includes:
- Pre-configured requests for all endpoints
- Example request/response bodies
- Test scripts for validation
- Automatic token management

### Using the Collection

1. Import `postman/Notes_API_Collection.json` into Postman
2. Set the `base_url` variable to your API URL
3. Run "Register User" first to create an account
4. Run "Login" to get an authentication token
5. The token is automatically saved for subsequent requests

## Production Deployment

### Recommended Hosting Platforms

- **Backend**: Render, Railway, Fly.io, or Azure App Service
- **Database**: Neon, Supabase, or Railway PostgreSQL

### Deployment Steps (Render Example)

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set environment variables in Render dashboard
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Environment Variables for Production

```bash
DATABASE_URL=postgresql://user:password@host:5432/database
SECRET_KEY=<generate-a-secure-random-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique email address
- `username`: Unique username
- `hashed_password`: Bcrypt hashed password
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Notes Table
- `id`: Primary key
- `title`: Note title
- `content`: Note content
- `owner_id`: Foreign key to users
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Note Versions Table
- `id`: Primary key
- `note_id`: Foreign key to notes
- `version_number`: Sequential version number
- `title`: Title snapshot
- `content`: Content snapshot
- `editor_id`: Foreign key to users (who made the change)
- `created_at`: Version creation timestamp

## License

This project is for educational purposes