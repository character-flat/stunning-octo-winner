import pytest
from fastapi import status


class TestGetVersions:
    """Tests for getting note versions."""

    def test_get_note_versions(self, client, auth_headers, test_note):
        """Test getting all versions of a note."""
        response = client.get(
            f"/api/v1/notes/{test_note.id}/versions",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["version_number"] == 1
        assert data[0]["note_id"] == test_note.id

    def test_get_versions_nonexistent_note(self, client, auth_headers):
        """Test getting versions of a nonexistent note returns 404."""
        response = client.get(
            "/api/v1/notes/99999/versions",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_specific_version(self, client, auth_headers, test_note):
        """Test getting a specific version of a note."""
        response = client.get(
            f"/api/v1/notes/{test_note.id}/versions/1",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["version_number"] == 1
        assert data["title"] == test_note.title
        assert data["content"] == test_note.content

    def test_get_nonexistent_version(self, client, auth_headers, test_note):
        """Test getting a nonexistent version returns 404."""
        response = client.get(
            f"/api/v1/notes/{test_note.id}/versions/999",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Version 999 not found" in response.json()["detail"]


class TestVersionCreation:
    """Tests for version creation on note updates."""

    def test_update_creates_new_version(self, client, auth_headers, test_note):
        """Test that updating a note creates a new version."""
        # Update the note
        client.put(
            f"/api/v1/notes/{test_note.id}",
            json={"title": "Updated Title", "content": "Updated content"},
            headers=auth_headers
        )

        # Get versions
        response = client.get(
            f"/api/v1/notes/{test_note.id}/versions",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 2  # Original + new version

        # Verify version 2 has the updated content
        version_2 = next((v for v in data if v["version_number"] == 2), None)
        assert version_2 is not None
        assert version_2["title"] == "Updated Title"
        assert version_2["content"] == "Updated content"

    def test_multiple_updates_create_versions(self, client, auth_headers, test_note):
        """Test that multiple updates create multiple versions."""
        # First update
        client.put(
            f"/api/v1/notes/{test_note.id}",
            json={"content": "First update"},
            headers=auth_headers
        )

        # Second update
        client.put(
            f"/api/v1/notes/{test_note.id}",
            json={"content": "Second update"},
            headers=auth_headers
        )

        # Get versions
        response = client.get(
            f"/api/v1/notes/{test_note.id}/versions",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 3  # Original + 2 updates


class TestRestoreVersion:
    """Tests for restoring notes to previous versions."""

    def test_restore_to_previous_version(self, client, auth_headers, test_note):
        """Test restoring a note to a previous version."""
        original_title = test_note.title
        original_content = test_note.content

        # Update the note
        client.put(
            f"/api/v1/notes/{test_note.id}",
            json={"title": "Changed Title", "content": "Changed content"},
            headers=auth_headers
        )

        # Restore to version 1
        response = client.post(
            f"/api/v1/notes/{test_note.id}/restore",
            json={"version_number": 1},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == original_title
        assert data["content"] == original_content

    def test_restore_creates_new_version(self, client, auth_headers, test_note):
        """Test that restoring creates a new version."""
        # Update the note
        client.put(
            f"/api/v1/notes/{test_note.id}",
            json={"content": "Updated content"},
            headers=auth_headers
        )

        # Restore to version 1
        client.post(
            f"/api/v1/notes/{test_note.id}/restore",
            json={"version_number": 1},
            headers=auth_headers
        )

        # Get versions
        response = client.get(
            f"/api/v1/notes/{test_note.id}/versions",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 3  # Original + update + restore

    def test_restore_nonexistent_version(self, client, auth_headers, test_note):
        """Test restoring to a nonexistent version returns 404."""
        response = client.post(
            f"/api/v1/notes/{test_note.id}/restore",
            json={"version_number": 999},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Version 999 not found" in response.json()["detail"]

    def test_restore_nonexistent_note(self, client, auth_headers):
        """Test restoring a nonexistent note returns 404."""
        response = client.post(
            "/api/v1/notes/99999/restore",
            json={"version_number": 1},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Note not found" in response.json()["detail"]

    def test_restore_no_auth(self, client, test_note):
        """Test restoring without authentication fails."""
        response = client.post(
            f"/api/v1/notes/{test_note.id}/restore",
            json={"version_number": 1}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
