# from django.test import TestCase
# from rest_framework.test import APIClient
# from django.contrib.auth.models import User
# from rest_framework_simplejwt.tokens import RefreshToken
# from pymongo import MongoClient
# import os
# import uuid
# from dotenv import load_dotenv
# load_dotenv()

# # MongoDB Configuration
# mongo_client = MongoClient(os.environ.get("mongo_url"))
# db = mongo_client.notes_db
# notes_collection = db.notes


# class NotesAPITestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#         # Create a test user instance
#         self.user = User.objects.create_user(
#             username="testuser",
#             password="Test@1234",
#             email="testuser@example.com"
#         )

#         # Generate JWT tokens for authentication
#         refresh = RefreshToken.for_user(self.user)
#         self.access_token = str(refresh.access_token)
#         self.client.credentials(
#             HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

#         # Example note data
#         self.note_data = {
#             "_id": str(uuid.uuid4()),
#             "user_id": self.user.id,
#             "title": "Test Note",
#             "content": "This is a test note content."
#         }
#         notes_collection.insert_one(self.note_data)

#     # def tearDown(self):
#     #     notes_collection.delete_many({})
#     #     db.users.delete_many({})

#     def test_get_notes_list(self):
#         response = self.client.get("/api/notes/")
#         print("Test Case1", response)
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(len(response.data) > 0)

#     def test_create_note(self):
#         new_note = {
#             "title": "New Test Note",
#             "content": "This is another test note."
#         }
#         response = self.client.post("/api/notes/", new_note, format="json")
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.data["note"]["title"], new_note["title"])

#     def test_get_note_detail(self):
#         response = self.client.get(f"/api/notes/{self.note_data['_id']}/")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data["title"], self.note_data["title"])

#     # def test_update_note(self):
#     #     updated_note = {
#     #         "title": "Updated Note",
#     #         "content": "Updated content for the note."
#     #     }
#     #     response = self.client.put(
#     #         f"/api/notes/{self.note_data['_id']}/", updated_note, format="json")
#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertEqual(response.data["message"],
#     #                      "Note updated successfully.")

#     # def test_delete_note(self):
#     #     response = self.client.delete(f"/api/notes/{self.note_data['_id']}/")
#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertEqual(response.data["message"],
#     #                      "Note deleted successfully.")

#     # def test_share_note(self):
#     #     share_data = {"shared_with": "anotheruser@example.com"}
#     #     response = self.client.post(
#     #         f"/api/notes/{self.note_data['_id']}/share/", share_data, format="json")
#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertEqual(response.data["message"], "Note shared successfully.")

#     # def test_search_notes(self):
#     #     response = self.client.get("/api/search/", {"q": "test"})
#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertTrue(len(response.data) > 0)
