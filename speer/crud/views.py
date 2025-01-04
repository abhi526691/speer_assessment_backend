import os
import uuid
from datetime import datetime
from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from dotenv import load_dotenv
from pymongo import MongoClient
from elasticsearch import Elasticsearch

load_dotenv()
username = os.environ.get("username")
password = os.environ.get("password")


mongo_client = MongoClient(
    "mongodb+srv://abhishek:abcd1234@speer.qdpo3.mongodb.net/notes_db?retryWrites=true&w=majority&appName=speer")

db = mongo_client.notes_db
notes_collection = db.notes

es_client = Elasticsearch(
    [{"host": "localhost", "port": 9200, "scheme": "http"}])


def index_note_to_es(note):
    es_client.index(index="notes", id=str(note["_id"]), body=note)


def delete_note_from_es(note_id):
    es_client.delete(index="notes", id=str(note_id))


class noteListAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = str(request.user.id)
        notes = list(notes_collection.find({"user_id": user_id}, {
                     "_id": 1, "title": 1, "content": 1, "date": 1}))
        for note in notes:
            note["_id"] = str(note["_id"])

        return Response({"notes": notes, "user_id": user_id}, status=status.HTTP_201_CREATED)

    def post(self, request):
        user_id = str(request.user.id)
        note = {
            "_id": str(uuid.uuid4()),
            "user_id": user_id,
            "title": request.data.get("title"),
            "content": request.data.get("content"),
            "date": datetime.now()
        }

        notes_collection.insert_one(note)
        # index_note_to_es(note)
        return Response({
            "message": "Note Created Successfully.",
            "note": note
        }, status=status.HTTP_201_CREATED)


class NoteDetailAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, note_id):
        user_id = str(request.user.id)
        note = notes_collection.find_one({"_id": note_id, "user_id": user_id})
        if not note:
            return Response({
                "error": "Note not found."
            }, status=status.HTTP_404_NOT_FOUND)
        note["_id"] = str(note["_id"])
        return Response({"note": note, "user_id": user_id}, status=status.HTTP_200_OK)

    def put(self, request, note_id):
        user_id = str(request.user.id)
        title = request.data.get("title", None)
        content = request.data.get("content", None)

        # Initialize the update_data dictionary
        update_data = {"date": datetime.now()}

        # Add keys conditionally based on their presence
        if title is not None:
            update_data["title"] = title
        if content is not None:
            update_data["content"] = content

        result = notes_collection.update_one({
            "_id": note_id,
            "user_id": user_id
        }, {"$set": update_data})

        if result.matched_count == 0:
            return Response({
                "error": "Note not found or you are not authorized."
            }, status=status.HTTP_401_UNAUTHORIZED)

        # updated_note = notes_collection.find_one({"_id": note_id})
        # index_note_to_es(updated_note)
        return Response({
            "message": "Note Updated Successfully"
        }, status=status.HTTP_200_OK)

    def delete(self, request, note_id):
        user_id = str(request.user.id)
        result = notes_collection.delete_one({
            "_id": note_id, "user_id": user_id
        })
        if result.deleted_count == 0:
            return Response({
                "error": "Note not found or you are not authorized"
            }, status=status.HTTP_401_UNAUTHORIZED)
        # delete_note_from_es(note_id)
        return Response({
            "message": "Note deleted successfully"
        }, status=status.HTTP_200_OK)


class ShareNoteAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, note_id):
        user_id = str(request.user.id)
        shared_with = request.data.get("shared_with")
        note = notes_collection.find_one({"_id": note_id, "user_id": user_id})
        if not note:
            return Response({
                "error": "Note not found or you are not authorized"
            }, status=status.HTTP_401_UNAUTHORIZED)

        notes_collection.update_one(
            {"_id": note_id}, {"$addToSet": {"shared_with": shared_with}})
        return Response({
            "message": "Notes Shared Successfully."
        }, status=status.HTTP_200_OK)


class SearchNotesAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = str(request.user.id)
        query = request.query_params.get("q")
        notes = list(notes_collection.find({"user_id": user_id, "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"content": {"$regex": query, "$options": "i"}}
        ]}, {"_id": 1, "title": 1, "content": 1}))

        if not notes:
            return Response({
                "error": f"No Notes found with the title {query}"
            }, status=status.HTTP_404_NOT_FOUND)

        for note in notes:
            note["_id"] = str(note["_id"])
        return Response(notes, status=status.HTTP_200_OK)
