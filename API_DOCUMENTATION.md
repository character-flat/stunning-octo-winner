# API Endpoints Documentation

## Overview

This document provides detailed information about the Notes API endpoints.

## Base URL

```
http://localhost:8000
```

## Endpoints

### 1. Health Check

#### Root Endpoint
- **URL**: `/`
- **Method**: `GET`
- **Description**: Root endpoint with API information
- **Response**:
```json
{
  "message": "Welcome to Notes API with Version History",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

#### Health Check
- **URL**: `/health`
- **Method**: `GET`
- **Description**: Health check endpoint
- **Response**:
```json
{
  "status": "healthy"
}
```

### 2. Notes Management

#### Create Note
- **URL**: `/notes/`
- **Method**: `POST`
- **Description**: Create a new note (automatically creates version 1)
- **Request Body**:
```json
{
  "title": "My Note Title",
  "content": "This is the content of my note."
}
```
- **Response** (201 Created):
```json
{
  "id": 1,
  "title": "My Note Title",
  "content": "This is the content of my note.",
  "created_at": "2026-01-07T07:13:45.000Z",
  "updated_at": "2026-01-07T07:13:45.000Z"
}
```

#### List Notes
- **URL**: `/notes/`
- **Method**: `GET`
- **Description**: List all notes with pagination
- **Query Parameters**:
  - `skip` (optional): Number of records to skip (default: 0)
  - `limit` (optional): Maximum number of records to return (default: 100)
- **Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "My Note Title",
    "content": "This is the content of my note.",
    "created_at": "2026-01-07T07:13:45.000Z",
    "updated_at": "2026-01-07T07:13:45.000Z"
  }
]
```

#### Get Note
- **URL**: `/notes/{note_id}`
- **Method**: `GET`
- **Description**: Get a specific note with its complete version history
- **Response** (200 OK):
```json
{
  "id": 1,
  "title": "My Note Title",
  "content": "This is the content of my note.",
  "created_at": "2026-01-07T07:13:45.000Z",
  "updated_at": "2026-01-07T07:13:45.000Z",
  "versions": [
    {
      "id": 1,
      "note_id": 1,
      "title": "My Note Title",
      "content": "This is the content of my note.",
      "version_number": 1,
      "created_at": "2026-01-07T07:13:45.000Z"
    }
  ]
}
```
- **Error Response** (404 Not Found):
```json
{
  "detail": "Note with id 999 not found"
}
```

#### Update Note
- **URL**: `/notes/{note_id}`
- **Method**: `PUT`
- **Description**: Update a note (automatically creates a new version)
- **Request Body** (all fields optional):
```json
{
  "title": "Updated Title",
  "content": "Updated content."
}
```
- **Response** (200 OK):
```json
{
  "id": 1,
  "title": "Updated Title",
  "content": "Updated content.",
  "created_at": "2026-01-07T07:13:45.000Z",
  "updated_at": "2026-01-07T07:15:30.000Z"
}
```
- **Error Response** (404 Not Found):
```json
{
  "detail": "Note with id 999 not found"
}
```

#### Delete Note
- **URL**: `/notes/{note_id}`
- **Method**: `DELETE`
- **Description**: Delete a note and all its versions (cascade delete)
- **Response**: 204 No Content
- **Error Response** (404 Not Found):
```json
{
  "detail": "Note with id 999 not found"
}
```

### 3. Version History

#### Get All Versions
- **URL**: `/notes/{note_id}/versions`
- **Method**: `GET`
- **Description**: Get all versions of a note (ordered by version number, descending)
- **Response** (200 OK):
```json
[
  {
    "id": 2,
    "note_id": 1,
    "title": "Updated Title",
    "content": "Updated content.",
    "version_number": 2,
    "created_at": "2026-01-07T07:15:30.000Z"
  },
  {
    "id": 1,
    "note_id": 1,
    "title": "My Note Title",
    "content": "This is the content of my note.",
    "version_number": 1,
    "created_at": "2026-01-07T07:13:45.000Z"
  }
]
```
- **Error Response** (404 Not Found):
```json
{
  "detail": "Note with id 999 not found"
}
```

#### Get Specific Version
- **URL**: `/notes/{note_id}/versions/{version_number}`
- **Method**: `GET`
- **Description**: Get a specific version of a note
- **Response** (200 OK):
```json
{
  "id": 1,
  "note_id": 1,
  "title": "My Note Title",
  "content": "This is the content of my note.",
  "version_number": 1,
  "created_at": "2026-01-07T07:13:45.000Z"
}
```
- **Error Responses**:
  - 404 Not Found (note doesn't exist):
    ```json
    {
      "detail": "Note with id 999 not found"
    }
    ```
  - 404 Not Found (version doesn't exist):
    ```json
    {
      "detail": "Version 99 not found for note 1"
    }
    ```

## Version History Behavior

### When is a version created?

1. **On Note Creation**: Version 1 is automatically created
2. **On Note Update**: A new version is created with an incremented version number

### Version Storage

Each version stores:
- The title at that point in time
- The content at that point in time
- The version number (sequential, starting from 1)
- The timestamp when the version was created

### Example Workflow

```
1. Create a note
   -> Note ID: 1, Version 1 created

2. Update the note (change title)
   -> Version 2 created with new title

3. Update the note (change content)
   -> Version 3 created with new content

4. Get all versions
   -> Returns versions 3, 2, 1 (newest first)

5. Get version 1
   -> Returns the original note content
```

## Error Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **204 No Content**: Resource deleted successfully
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation error

## Interactive Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- View all endpoints
- See request/response schemas
- Test endpoints directly from the browser
- View example requests and responses
