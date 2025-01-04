# Django Notes Application with JWT Authentication and MongoDB

This project is a Django-based API application that implements user authentication using JWT (JSON Web Tokens) and provides CRUD functionality for notes. The application uses Django's default SQLite database for user data storage and MongoDB Cloud for storing the notes. Rate limiting is implemented using Django's default throttling mechanism.

## Features

- User authentication using JWT tokens.
- User registration and login with email and password.
- CRUD functionality for notes (Create, Read, Update, Delete).
- Notes are stored in MongoDB Cloud.
- Search functionality for notes based on title or content.
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
git clone <repository-url>
cd <repository-folder>
```
