# IHR FastAPI App

This project is a FastAPI-based backend for the IHR system. It is designed for flexibility and can be run either in a **Python virtual environment** or using **Docker**.

---

##  Getting Started

### 1. Clone the Repository

### 2. Create a `.env` File

In the project root directory, create a new `.env` file to define your specific database connection string.

`.env` content:

```env
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database>
```


---

## Running the Application

You can run this application in one of the following ways:

* Using a Python virtual environment
* Using Docker

---

## Option 1: Run in a Python Virtual Environment

### Step 1: Create and Activate a Virtual Environment

#### On Windows:

```sh
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:

```sh
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```sh
pip install -r requirements.txt
```

### Step 3: Run the Application

```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### **Step 4: Access the API**
Once running, you can access:
- API: **[http://localhost:8000](http://localhost:8000)**
- Interactive Docs (Swagger UI): **[http://localhost:8000/docs](http://localhost:8000/docs)**
- Redoc Docs: **[http://localhost:8000/redoc](http://localhost:8000/redoc)**

---

## Option 2: Run with Docker

### Step 1: Build the Docker Image

```sh
docker build -t ihr-fastapi .
```

### Step 2: Run the Docker Container

```sh
docker run -p 8000:8000 --env-file .env ihr-fastapi
```

### (Optional) Step 3: Manage the Container

Start an existing container:

```sh
docker start <container-id>
```

View logs:

```sh
docker logs -f <container-id>
```

### Step 4: Access the API

Once running, you can access:
- API: **[http://localhost:8000](http://localhost:8000)**
- Interactive Docs (Swagger UI): **[http://localhost:8000/docs](http://localhost:8000/docs)**
- Redoc Docs: **[http://localhost:8000/redoc](http://localhost:8000/redoc)**

---

# Documentation

The `docs/` folder contains detailed documentation for various aspects of the project. Below is a list of available documentation files and their descriptions:

### 1. [Project Structure](docs/project_structure.md)
Provides an overview of the project's file and folder structure, organized according to the **Service-Controller-Repository** architectural pattern.

### 2. [Project Architecture](docs/project_architecture.md)
Explains the **Service-Controller-Repository** architecture adopted by the project, highlighting the responsibilities of each layer and how they interact.

### 3. [Database Migration](docs/database_migration.md)
Details how to manage database migrations using Alembic, including TimescaleDB-specific features like hypertables and compression policies.

### 4. [Adding a New Endpoint](docs/add_new_endpoint.md)
A step-by-step guide on how to add a new endpoint to the application.


