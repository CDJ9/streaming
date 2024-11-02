
# Str3aming Backend

This is the backend service for the **Str3aming web application**, built using **FastAPI** and **MySQL**. The backend handles **user authentication** and **room management** functionalities, enabling users to sign up, log in, and create rooms for video conferencing.

---

## **Table of Contents**
- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [API Documentation](#api-documentation)
- [How to Run the App](#how-to-run-the-app)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [Contributors](#contributors)

---

## **Overview**

The **Str3aming Backend** provides the following key features:
- **User Authentication:** Users can register and log in.
- **Room Management:** Users can create video conferencing rooms.
- **Swagger Documentation:** Provides an interactive interface to test the API.
- **Database Integration:** Uses MySQL to store user and room data.

---

## **Technologies Used**

- **Python 3.10+**
- **FastAPI** - Web framework for building APIs.
- **Uvicorn** - ASGI server for running FastAPI apps.
- **MySQL** - Relational database management system.
- **SQLAlchemy** - ORM for interacting with the database.
- **Pydantic Settings** - For managing environment variables.
- **PyMySQL** - MySQL database driver for Python.

---

## **Project Structure**

```
backend/
│
├── app/
│   ├── __init__.py               # Marks the folder as a Python package
│   ├── main.py                   # Entry point of the FastAPI application
│   ├── dependencies.py           # SQLAlchemy engine and session logic
│   ├── models.py                 # Database models (Users and Rooms)
│   ├── routers/                  # Folder for route handlers
│   │   ├── __init__.py
│   │   ├── auth.py               # Authentication routes
│   │   └── room.py               # Room management routes
│   ├── config/                   # App configuration files
│   │   ├── __init__.py
│   │   └── settings.py           # Loads environment variables
│   └── services/                 # Optional folder for service logic
│       └── __init__.py
├── .env                          # Environment variables file
├── requirements.txt              # List of dependencies
├── venv/                         # Virtual environment folder (optional)
└── README.md                     # Project documentation
```

---

## **Setup Instructions**

### 1. Clone the Repository
```bash
git clone <repository-url>
cd backend
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
```

Activate the virtual environment:

- **Windows**:
  ```bash
  .\venv\Scripts\activate
  ```

- **Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## **Environment Variables**

Create a **`.env`** file in the project root with the following content:

```
DATABASE_URL=mysql+pymysql://jitsi_user:yourpassword@localhost/str3aming
SECRET_KEY=your-secret-key
JITSI_DOMAIN=https://meet.jit.si
```

- Replace `yourpassword` with your MySQL user password.
- Set `SECRET_KEY` to a random, secure string for JWT tokens.

---

## **Database Setup**

1. **Log into MySQL**:
   ```bash
   mysql -u root -p
   ```

2. **Create the `str3aming` database**:
   ```sql
   CREATE DATABASE str3aming;
   ```

3. **Create a MySQL user and grant privileges**:
   ```sql
   CREATE USER 'jitsi_user'@'localhost' IDENTIFIED BY 'yourpassword';
   GRANT ALL PRIVILEGES ON str3aming.* TO 'jitsi_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. **Verify the user and database**:
   ```sql
   SHOW DATABASES;
   SELECT user, host FROM mysql.user;
   ```

---

## **API Documentation**

Access the **Swagger UI** to explore the API:
```
http://127.0.0.1:8000/docs
```

### **Auth Routes:**
- **POST /auth/signup**  
  **Request Body:**
  ```json
  {
    "username": "testuser",
    "password": "password123",
    "email": "testuser@example.com"
  }
  ```

- **POST /auth/login**  
  **Request Body:**
  ```json
  {
    "username": "testuser",
    "password": "password123"
  }
  ```

### **Room Routes:**
- **POST /room/create**  
  **Request Body:**
  ```json
  {
    "room_name": "myroom",
    "user_name": "testuser"
  }
  ```

---

## **How to Run the App**

1. **Start the FastAPI server**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the Swagger UI**:
   ```
   http://127.0.0.1:8000/docs
   ```

3. **Test the API endpoints** using the Swagger UI.

---

## **Troubleshooting**

- **Access Denied for MySQL User**:
  - Ensure the MySQL user credentials are correct and the user has privileges on the `str3aming` database.

- **App Not Found on Root URL**:
  - Ensure a root route (`/`) is defined in `main.py`:
    ```python
    @app.get("/")
    def read_root():
        return {"message": "Welcome to Str3aming Backend!"}
    ```

- **Changes Not Reflecting**:
  - Make sure you are running the server with the `--reload` option:
    ```bash
    uvicorn app.main:app --reload
    ```

---

## **Future Improvements**

- **JWT Authentication**: Add JWT tokens to protect routes.
- **Persistent Room Storage**: Store timestamps for room creation and access history.
- **WebSocket Integration**: Enable real-time communication using WebSockets.
- **Video Conferencing Integration**: Use Jitsi API for live video rooms.

---

## **Contributors**

- **Your Name** - Project Lead  
- **Your Partner's Name** - Backend Developer

---

## **License**

This project is licensed under the MIT License.
