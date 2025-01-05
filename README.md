# Django Notes Application with JWT Authentication and MongoDB

This project is a Django-based API application that implements user authentication using JWT (JSON Web Tokens) and provides CRUD functionality for notes. The application uses Django's default SQLite database for user data storage and MongoDB Cloud for storing the notes. Rate limiting is implemented using Django's default throttling mechanism.

## Features

- User authentication using JWT tokens.
- User registration and login with email and password.
- CRUD functionality for notes (Create, Read, Update, Delete).
- Notes are stored in MongoDB Cloud.
- Search functionality for notes based on title or content.(P.S. Elastic Search + indexing is preferred for document based database(mongodb) since document based can make searching slower
- Throttling for rate limiting using Django's default throttling classes.

## Requirements

- Python 3.8 or later
- Django 5.1
- Django REST Framework
- JWT Authentication (using `djangorestframework-simplejwt`)
- MongoDB Cloud (Atlas)
- Elasticsearch (optional for search feature)
- dotenv for environment variable management

## Setup

Follow the steps below to set up and run the application.

### 1. Clone the repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/abhi526691/speer_assessment_backend
cd speer_assessment_backend 
```

### 2. Create a virtual enviornment

create the virtual environment to manage dependencies:

```bash
python3 -m venv speer
source speer\Scripts\activate
```

### 3. Install dependencies

Install the required dependencies from the requirements.txt file:

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a .env file in the root directory of the project. Add the following content to specify your MongoDB connection URL:

```bash
mongo_url=<your_mongodb_connection_url>
```
You can get your MongoDB connection URL from <a href="https://www.mongodb.com/products/platform/atlas-database">MongoDB Atlas.</a>

### 5. Migrate the database

Django uses SQLite as the default database for user authentication data. Run the migrations to set up the database:

```bash
python manage.py migrate
```

### 6. Run the server
Start the Django development server:

```bash
python manage.py runserver
```
The application will be available at http://127.0.0.1:8000/.

### 6. Test the Endpoints

Django's default TestCase Library is used for testing the Endpoints. Simply run the below command to test the endpoints

```bash
python manage.py test
```

### API Endpoints
Authentication
###### 1. POST /api/auth/signup/: Create a new user.
  . Request body:
   ```bash
    {
    "username": "new_user",
    "email": "new_user@example.com",
    "password": "Password123!"
    }
```
Password must have at least 1 special character, 1 uppercase, and length must be greater than 10

. POST /api/auth/login/: Login with email and password to get JWT tokens.
Request body:
   ```bash
{
    "email": "user@example.com",
    "password": "Password123!"
}
```
. Response:
   ```bash
{
    "user_id": 1,
    "refresh": "your-refresh-token",
    "access": "your-access-token"
}
```

### Notes CRUD Operations
1. GET /api/notes/: Get all notes for the authenticated user.
2. POST /api/notes/: Create a new note.
   ```bash
   {
    "title": "Note title",
    "content": "Note content"
   }
   ```
1. GET /api/notes/<note_id>/: Get details of a specific note.
2. PUT /api/notes/<note_id>/: Update an existing note.
      ```bash
    {
    "title": "Updated note title",
    "content": "Updated note content"
    }
   ```
1. DELETE /api/notes/<note_id>/: Delete a note.
2. POST /api/notes/<note_id>/share/: Share a note with another user.
      ```bash
    {
    "shared_with": "user_id_to_share_with"
    }
   ```

##### Search Notes
. GET /api/search/: Search for notes based on title or content.
. Query parameter: q (search query).



### Throttling
This application uses Django's default throttling to limit the rate of requests:
. AnonRateThrottle: Limits unauthenticated users' requests.
. UserRateThrottle: Limits authenticated users' requests.

### Technologies Used
1. Django: Web framework for building the API.
2. Django REST Framework: For building the REST API.
3. djangorestframework-simplejwt: For JWT authentication.
4. MongoDB Cloud: For storing CRUD data.
5. Elasticsearch: (Optional) For searching notes.
6. Python 3: Programming language.





