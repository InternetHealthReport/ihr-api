# Project Structure

This document provides an overview of the project's file and folder structure. Each part of the application is organized according to the **Service-Controller-Repository** architectural pattern for better maintainability, modularity, and scalability.

## 📁 Project Tree

```plaintext
.
├── alembic/               # Database migration scripts 
├── config/                # App configuration
├── controllers/           # API endpoints and HTTP route handlers (Controller Layer)
├── docs/                  # Documentation files
├── dtos/                  # Data Transfer Objects for request/response schemas
├── models/                # Database models and ORM classes (Model Layer)
├── repositories/          # Data access logic and database interaction (Repository Layer)
├── services/              # Business logic layer (Service Layer)
├── .env                   # Environment variables (e.g., database credentials)
├── .gitignore             # Specifies intentionally untracked files to ignore
├── alembic.ini            # Alembic configuration file
├── dockerfile             # Docker image instructions to build the app container
├── globals.py             # Global constants
├── main.py                # FastAPI entry point (starts the app)
├── README.md              # Project documentation 
├── requirements.txt       # Python dependencies list for pip installation

````
