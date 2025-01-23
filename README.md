CRUD Backend API using FastAPI

This repository contains a fully functional backend API built using FastAPI. The API performs CRUD (Create, Read, Update, Delete) operations for users and posts and implements authentication mechanisms using JSON Web Tokens (JWT). The project is designed as a generalized template and can be modified to suit various application needs.

Features

CRUD Operations: Create, retrieve, update, and delete users and posts.

Authentication: Login functionality implemented using JWT for secure access.

Database Integration: PostgreSQL is used as the database, with the psycopg2 driver to manage database connections.

Modular Design: The application is organized into separate files and directories for scalability and readability.

Project Structure

app/
├── config.py      # Configuration file for database and other settings
├── database.py    # Database connection setup
├── main.py        # Entry point for the application
├── model.py       # Pydantic models
├── oauth2.py      # JWT authentication logic
├── schema.py      # Database schemas
├── utils.py       # Utility functions (e.g., password hashing)
├── routers/       # Directory containing route handlers
│   ├── auth.py    # Routes for authentication (login)
│   ├── post.py    # Routes for CRUD operations on posts
│   ├── user.py    # Routes for CRUD operations on users
│   ├── vote.py    # Routes for handling votes on posts
