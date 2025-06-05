# FastAPI Application

This project is IHR FastAPI-based application. You can run it either in a **Python virtual environment** or using **Docker**.

---

## Running the Application

You can run this application in two ways:
1. **Using a Python Virtual Environment**
2. **Using Docker**

---

## 1. Running in a Virtual Environment

### **1️⃣ Create and Activate a Virtual Environment**
#### On Windows (Command Prompt or PowerShell):
```sh
python3 -m venv venv
venv\Scripts\activate
```
#### On macOS/Linux:
```sh
python3 -m venv venv
source venv/bin/activate
```

### **2️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **3️⃣ Run the FastAPI Application**
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### **4️⃣ Access the API**
Once running, you can access:
- API: **[http://localhost:8000/ihr/api](http://localhost:8000/ihr/api)**
- Interactive Docs (Swagger UI): **[http://localhost:8000/ihr/api/docs](http://localhost:8000/docs)**
- Redoc Docs: **[http://localhost:8000/ihr/api/redoc](http://localhost:8000/redoc)**

---

## 🐳 2. Running with Docker

### **1️⃣ Build the Docker Image**
```sh
docker build -t ihr-fastapi .
```

### **2️⃣ Run the Container**
```sh
docker run -p 8000:8000 ihr-fastapi
```

### **3️⃣ start the Container**
```sh
docker start <container-id>
# Attach to the logs
docker logs -f <container-id>
```


### **3️⃣ Access the API**
Once running, you can access:
- API: **[http://localhost:8000/ihr/api](http://localhost:8000/ihr/api)**
- Interactive Docs (Swagger UI): **[http://localhost:8000/ihr/api/docs](http://localhost:8000/docs)**
- Redoc Docs: **[http://localhost:8000/ihr/api/redoc](http://localhost:8000/redoc)**


