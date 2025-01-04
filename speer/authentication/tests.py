from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
import mongomock
from unittest.mock import patch
from datetime import datetime
import uuid

# Mock MongoDB
mock_mongo_client = mongomock.MongoClient()


@patch('speer.MongoClient', return_value=mock_mongo_client)
class APITestCase(TestCase):
    def setUp(self):
        # Initialize API client
        self.client = APIClient()

        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123")

        # Mock MongoDB collection
        self.notes_collection = mock_mongo_client.notes_db.notes

        # Login and get tokens
        self.client.post('/api/auth/signup/', {"username": "testuser",
                         "email": "test@example.com", "password": "password123"})
        login_response = self.client.post(
            '/login/', {"email": "test@example.com", "password": "password123"})
        self.access_token = login_response.data['access']
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_signup(self):
        response = self.client.post('/api/auth/signup/', {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

    def test_login(self):
        response = self.client.post('/api/auth/login/', {
            "email": "test@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_create_note(self):
        response = self.client.post('/api/notes/', {
            "title": "Test Note",
            "content": "This is a test note."
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)

    def test_get_notes(self):
        # Insert a test note
        note = {
            "_id": str(uuid.uuid4()),
            "user_id": str(self.user.id),
            "title": "Test Note",
            "content": "This is a test note.",
            "date": datetime.now()
        }
        self.notes_collection.insert_one(note)

        response = self.client.get('/api/notes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data["notes"]), 0)

    def test_get_note_detail(self):
        # Insert a test note
        note_id = str(uuid.uuid4())
        note = {
            "_id": note_id,
            "user_id": str(self.user.id),
            "title": "Test Note",
            "content": "This is a test note.",
            "date": datetime.now()
        }
        self.notes_collection.insert_one(note)

        response = self.client.get(f'/api/notes/{note_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("note", response.data)

    def test_update_note(self):
        # Insert a test note
        note_id = str(uuid.uuid4())
        note = {
            "_id": note_id,
            "user_id": str(self.user.id),
            "title": "Test Note",
            "content": "This is a test note.",
            "date": datetime.now()
        }
        self.notes_collection.insert_one(note)

        response = self.client.put(f'/api/notes/{note_id}/', {
            "title": "Updated Note",
            "content": "Updated content."
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

    def test_delete_note(self):
        # Insert a test note
        note_id = str(uuid.uuid4())
        note = {
            "_id": note_id,
            "user_id": str(self.user.id),
            "title": "Test Note",
            "content": "This is a test note.",
            "date": datetime.now()
        }
        self.notes_collection.insert_one(note)

        response = self.client.delete(f'/api/notes/{note_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

    def test_search_notes(self):
        # Insert a test note
        note = {
            "_id": str(uuid.uuid4()),
            "user_id": str(self.user.id),
            "title": "Search Test",
            "content": "Searchable content.",
            "date": datetime.now()
        }
        self.notes_collection.insert_one(note)

        response = self.client.get('/notes/search/?q=Search')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_share_note(self):
        # Insert a test note
        note_id = str(uuid.uuid4())
        note = {
            "_id": note_id,
            "user_id": str(self.user.id),
            "title": "Share Test",
            "content": "This note will be shared.",
            "date": datetime.now()
        }
        self.notes_collection.insert_one(note)

        response = self.client.post(f'/notes/{note_id}/share/', {
            "shared_with": "anotheruser@example.com"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
