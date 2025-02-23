# 🍔BiteMe: Food Ordering System
## Overview

BiteMe is a microservices-based food ordering platform that provides personalized menu recommendations using Gemini AI. It features a FastAPI backend, React frontend, and MongoDB database, supporting guest users, logged-in users, and admins. The system is containerized with Docker, ensuring scalability and seamless interactions between services. 🚀

![_png biteme logo (1)](https://github.com/user-attachments/assets/f7eed7ed-b51a-4a71-8b0e-5cec53db5d64)

---

## 🌟 Key Features

- 🔐 User Authentication
  - Secure user registration
  - JWT-based login system
  - User profile management

- 🍽️ Restaurant Management
  - Create and manage restaurant profiles
  - Add, update, and delete menu items
  - Filter restaurants by cuisine and rating

- 🛒 Order Processing
  - Create and track food orders
  - Retrieve user-specific order history
  - Update order status

- 🔒 Security Features
  - Password hashing
  - Token-based authentication
  - Role-based access control
    
- 🧠 AI-Powered Recommendations
  - Personalized food suggestions using Gemini AI
  - Recommendations based on order history and preferences
  - Recommendations based on time of the day

---
## Architecture Diagram:
![Architecture Diagram](https://github.com/user-attachments/assets/67ad1f0f-819a-4b61-b08d-9af41ec1990e)

---

## 🛠️ Technologies Used

- **Backend**: FastAPI, Pydantic, PyMongo
- **Database**: MongoDB
- **Frontend**: React, JavaScript, HTML, CSS
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: pytest
- **Docke**: Containerization for microservices
- **Gemini AI**: AI-powered menu recommendations

---

## 📂 Project Structure

```plaintext
RealBiteMe/
│── backend/                   # FastAPI backend services
│── frontend/                  # Frontend application
│── menu-recommendations-service/  # AI-driven recommendation engine
│── .gitignore                 # Git ignore file
│── .env                       # Environment variables
│── README.md                  # Project documentation

```

---
## 📋 System Requirements

### Prerequisites:
- Python 3.9+
- MongoDB
- pip and virtualenv (for Python dependency management)
- Docker: Required for microservices integration
-Node.js 16+ (for frontend)

  
---

## **👄 Installation**
## 🔧 Installation

### 1. Clone the Repository
```
git clone <repository-url>
cd RealBiteMe
```

 **2. Create Virtual Environment:**
```
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
 ```


 **3. Install Dependencies:**
   ```
pip install -r requirements.txt
 ```


**4. Configure Environment Variables**
Create a .env file in the project root with:
```
MONGO_URI=your_mongodb_connection_string
SECRET_KEY=your_secret_key
```

---

## ▶️ **🚀 Running the Application**

Development Mode

```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Production Deployment
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## **🧬 🧪 Testing**

```
pytest
```
Test Coverage

Unit Tests: Model validations, security functions
Integration Tests: User registration, restaurant management, order processing
---

## **🐋 Docker Support**

1. **Build the Docker Image:**
 ```
docker build -t biteme-backend .
   ```
2. **Run the Docker Container:**
```
docker run -d -p 8000:8000 biteme-backend
   ```
---
## 📚 API Documentation

Access Swagger UI for interactive API documentation:

URL: http://localhost:8000/docs
Explore and test all endpoints directly in your browser


---

## 🙌 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

Michelle Cain

email:michellecainn@gmail.com

