# Productivity App – Flask Backend

## Overview

This project is the backend API for a Productivity App built using Flask and SQLAlchemy.

The application allows users to create accounts, authenticate securely using JSON Web Tokens (JWT), and manage personal notes.

Each user can only access and manage their own notes.

## Technologies Used

- Python 3.8
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Flask-JWT-Extended
- Flask-CORS
- SQLite
- Marshmallow
- Faker
- Pytest

## Features

### Authentication
- User registration.
- User login.
- Password hashing using bcrypt.
- JWT-based authentication.
- Retrieve authenticated user information.
- Protected API endpoints.

### Notes Management
- Create notes.
- Retrieve all personal notes.
- Retrieve a single note.
- Update notes.
- Delete notes.
- Pagination.
- User ownership protection.

## Project Structure

```text
server/
├── app.py
├── config.py
├── extensions.py
├── models.py
├── seed.py
├── migrations/
├── resources/
│   ├── __init__.py
│   ├── auth.py
│   └── notes.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_notes.py
├── .env.example
├── .gitignore
├── Pipfile
├── Pipfile.lock
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/flask-c10-summative-lab-sessions-and-jwt-clients.git
```

### 2. Navigate to the server directory

```bash
cd flask-c10-summative-lab-sessions-and-jwt-clients/server
```

### 3. Install dependencies

Install Pipenv if necessary:

```bash
pip install pipenv
```

Install project dependencies:

```bash
pipenv install
```

### 4. Configure environment variables

Create your environment file:

```bash
cp .env.example .env
```

Configure your secret keys and database URL in `.env`.

Example:

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///productivity.db
```

Never commit your actual `.env` file or expose your secret keys.

### 5. Set up the database

Run database migrations:

```bash
pipenv run flask --app app.py db upgrade
```

### 6. Seed the database

Populate the database with sample users and notes:

```bash
pipenv run python seed.py
```

Demo credentials:

- Username: `demo_user1` through `demo_user5`
- Password: `Password123!`

These credentials are intended for local development and testing only.

### 7. Start the Flask server

```bash
pipenv run python app.py
```

The backend runs at:

```text
http://127.0.0.1:5555
```

## API Endpoints

All endpoints return JSON responses.

### Authentication

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/signup` | Register a new user | No |
| POST | `/login` | Authenticate a user | No |
| GET | `/me` | Retrieve current user | JWT required |

#### Signup request

```json
{
    "username": "peter",
    "password": "Password123!",
    "password_confirmation": "Password123!"
}
```

#### Login request

```json
{
    "username": "peter",
    "password": "Password123!"
}
```

Successful authentication returns a JWT token and user information.

### Notes

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| GET | `/notes` | Retrieve all personal notes | JWT required |
| POST | `/notes` | Create a note | JWT required |
| GET | `/notes/<id>` | Retrieve a specific note | JWT required |
| PATCH | `/notes/<id>` | Update a note | JWT required |
| DELETE | `/notes/<id>` | Delete a note | JWT required |

### Creating a note

```json
{
    "title": "My First Note",
    "content": "Learning Flask and JWT authentication."
}
```

### Updating a note

```json
{
    "title": "Updated Note"
}
```

### Pagination

The notes endpoint supports pagination.

Example:

```text
GET /notes?page=1&per_page=5
```

The response includes notes and pagination information.

## Authentication and Security

The application uses JWT access tokens to protect private endpoints.

Include the token in the request header:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Passwords are hashed using Flask-Bcrypt before being stored in the database.

Users can only access notes associated with their authenticated user ID.

## Frontend Integration

The backend is configured to work with the React JWT client.

Frontend URL:

```text
http://localhost:4000
```

Backend URL:

```text
http://localhost:5555
```

CORS is configured to allow requests from the React frontend.

## Running Automated Tests

Run all tests:

```bash
pipenv run pytest -v
```

The test suite covers:

- User registration.
- Login and authentication.
- JWT protection.
- Notes creation and retrieval.
- Notes updating and deletion.
- Resource ownership protection.
- Unauthorized access.

## Database Migrations

Create a new migration after changing database models:

```bash
pipenv run flask --app app.py db migrate -m "Describe your changes"
```

Apply migrations:

```bash
pipenv run flask --app app.py db upgrade
```

## Author

Developed as part of the Moringa School Software Engineering Bootcamp.
