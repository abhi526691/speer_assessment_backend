from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from pymongo import MongoClient
import os
from datetime import datetime
import uuid


class NotesAPITestCase(TestCase):
    def setUp(self):
        # Set up test user
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="Password123!")
        self.client.force_authenticate(user=self.user)

        # Set up MongoDB connection
        self.mongo_client = MongoClient(os.environ.get("mongo_url"))
        self.notes_collection = self.mongo_client.notes_db.notes

        self.notes_url = '/api/notes/'
        self.note_id = str(self.notes_collection.insert_one({
            "_id": str(uuid.uuid4()),
            "user_id": str(self.user.id),
            "title": "Test Note",
            "content": "Test Content",
            "date": datetime.now()
        }).inserted_id)

    def tearDown(self):
        self.notes_collection.delete_many({})

    def test_create_note(self):
        response = self.client.post(self.notes_url, {
            "title": "New Note",
            "content": "Note content"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("note", response.data)

    def test_get_notes(self):
        response = self.client.get(self.notes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("notes", response.data)

    def test_get_note_detail(self):
        response = self.client.get(f'/api/notes/{str(self.note_id)}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("note", response.data)

    def test_update_note(self):
        response = self.client.put(f'/api/notes/{self.note_id}/', {
            "title": "Updated Title",
            "content": "Updated Content"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Note Updated Successfully")

    def test_delete_note(self):
        note_id = str(self.notes_collection.insert_one({
            "_id": str(uuid.uuid4()),
            "user_id": str(self.user.id),
            "title": "Deleting Test Note",
            "content": "Deleting Test Content",
            "date": datetime.now()
        }).inserted_id)
        response = self.client.delete(f'/api/notes/{note_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Note deleted successfully")

    def test_share_note(self):
        response = self.client.post(f'/api/notes/{self.note_id}/share/', {
            "shared_with": "2"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"],
                         "Notes Shared Successfully.")

    def test_search_notes(self):
        response = self.client.get(f'/api/search/?q=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
