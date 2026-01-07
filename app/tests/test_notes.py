import pytest
from fastapi import status


class TestCreateNote:
    """Tests for note creation endpoint."""

    def test_create_note_success(self, client, auth_headers):
        """Test successful note creation."""
        response = client.post(
            "/api/v1/notes/",
            json={"title": "My Note", "content": "My note content"},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "My Note"
        assert data["content"] == "My note content"
        assert "id" in data
        assert "owner_id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_note_no_auth(self, client):
        """Test note creation without authentication fails."""
        response = client.post(
            "/api/v1/notes/",
            json={"title": "My Note", "content": "My note content"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_note_missing_title(self, client, auth_headers):
        """Test note creation without title fails."""
        response = client.post(
            "/api/v1/notes/",
            json={"content": "My note content"},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_note_empty_title(self, client, auth_headers):
        """Test note creation with empty title fails."""
        response = client.post(
            "/api/v1/notes/",
            json={"title": "", "content": "My note content"},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetNotes:
    """Tests for fetching notes endpoints."""

    def test_get_all_notes(self, client, auth_headers, test_note):
        """Test getting all notes for current user."""
        response = client.get("/api/v1/notes/", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["title"] == test_note.title

    def test_get_notes_no_auth(self, client):
        """Test getting notes without authentication fails."""
        response = client.get("/api/v1/notes/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_single_note(self, client, auth_headers, test_note):
        """Test getting a single note by ID."""
        response = client.get(f"/api/v1/notes/{test_note.id}", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_note.id
        assert data["title"] == test_note.title
        assert data["content"] == test_note.content

    def test_get_nonexistent_note(self, client, auth_headers):
        """Test getting a nonexistent note returns 404."""
        response = client.get("/api/v1/notes/99999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Note not found" in response.json()["detail"]


class TestUpdateNote:
    """Tests for note update endpoint."""

    def test_update_note_title(self, client, auth_headers, test_note):
        """Test updating note title."""
        response = client.put(
            f"/api/v1/notes/{test_note.id}",
            json={"title": "Updated Title"},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["content"] == test_note.content

    def test_update_note_content(self, client, auth_headers, test_note):
        """Test updating note content."""
        response = client.put(
            f"/api/v1/notes/{test_note.id}",
            json={"content": "Updated content"},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["content"] == "Updated content"

    def test_update_note_both_fields(self, client, auth_headers, test_note):
        """Test updating both title and content."""
        response = client.put(
            f"/api/v1/notes/{test_note.id}",
            json={"title": "New Title", "content": "New content"},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "New Title"
        assert data["content"] == "New content"

    def test_update_nonexistent_note(self, client, auth_headers):
        """Test updating a nonexistent note returns 404."""
        response = client.put(
            "/api/v1/notes/99999",
            json={"title": "New Title"},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_note_no_auth(self, client, test_note):
        """Test updating note without authentication fails."""
        response = client.put(
            f"/api/v1/notes/{test_note.id}",
            json={"title": "New Title"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestDeleteNote:
    """Tests for note deletion endpoint."""

    def test_delete_note(self, client, auth_headers, test_note):
        """Test deleting a note."""
        response = client.delete(f"/api/v1/notes/{test_note.id}", headers=auth_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify note is deleted
        get_response = client.get(f"/api/v1/notes/{test_note.id}", headers=auth_headers)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_note(self, client, auth_headers):
        """Test deleting a nonexistent note returns 404."""
        response = client.delete("/api/v1/notes/99999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_note_no_auth(self, client, test_note):
        """Test deleting note without authentication fails."""
        response = client.delete(f"/api/v1/notes/{test_note.id}")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
