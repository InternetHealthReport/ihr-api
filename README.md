# IHR FastAPI App

This project is a FastAPI-based backend for the IHR system. It is designed for flexibility and can be run either in a **Python virtual environment** or using **Docker**.

---

##  Getting Started

### 1. Clone the Repository

### 2. Create a `.env` File

In the project root directory, create a `.env` file to define environment-specific settings, including the database connection.

Example `.env` content:

```env
DATABASE_URL=postgresql://postgres:123password456@localhost:5435/ihr-fastapi
```

> Make sure PostgreSQL is running and the database exists before continuing.

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
- API: **[http://localhost:8000/ihr/api](http://localhost:8000/ihr/api)**
- Interactive Docs (Swagger UI): **[http://localhost:8000/ihr/api/docs](http://localhost:8000/docs)**
- Redoc Docs: **[http://localhost:8000/ihr/api/redoc](http://localhost:8000/redoc)**

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
- API: **[http://localhost:8000/ihr/api](http://localhost:8000/ihr/api)**
- Interactive Docs (Swagger UI): **[http://localhost:8000/ihr/api/docs](http://localhost:8000/docs)**
- Redoc Docs: **[http://localhost:8000/ihr/api/redoc](http://localhost:8000/redoc)**
