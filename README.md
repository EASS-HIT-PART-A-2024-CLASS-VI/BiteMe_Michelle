# 🍔BiteMe: Food Ordering System
This repository contains the code for a Food Ordering System that allows users to order food online, manage menu items, and handle food orders efficiently. The backend is built using FastAPI and follows SOLID principles for clean and modular design.
![_png biteme logo (1)](https://github.com/user-attachments/assets/f7eed7ed-b51a-4a71-8b0e-5cec53db5d64)

---

## 🌟 Key Features

### Backend Capabilities:
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
---

## 🛠️ Technologies Used

### Backend Stack:
- **Web Framework**: FastAPI
- **Database**: MongoDB
- **ORM/Validation**: Pydantic
- **Authentication**: JWT (JSON Web Tokens)
- **Database Driver**: PyMongo
- **Testing**: pytest

---

## 📂 Project Structure

```plaintext
..
backend/
├── app/
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   ├── orders.py
│   │   ├── restaurants.py
│   │   └── users.py
│   ├── core/               # Core configurations
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── dbConnection/       # Database connectivity
│   │   └── mongoRepository.py
│   ├── models/            # Data models
│   │   ├── __init__.py
│   │   └── models.py
│   └── main.py
├── tests/                 # Test files
│   ├── __init__.py
│   ├── conftest.py
│   ├── integration_test.py
│   └── unit_test.py
├── Dockerfile            # Docker configuration
├── README.md
└── requirements.txt      # Project dependencies

```

---
## 📋 System Requirements

### Prerequisites:
- Python 3.9+
- MongoDB
- pip package manager
---

## **👄 Installation**
## 🔧 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/EASS-HIT-PART-A-2024-CLASS-VI/BiteMe.git
cd BiteMe/backend   ```

 **2. Create Virtual Environment:**
```
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate` ```


 **3. Install Dependencies:**
   ```
pip install -r requirements.txt   ```


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
📚 API Documentation
Access Swagger UI for interactive API documentation:

URL: http://localhost:8000/docs
Explore and test all endpoints directly in your browser

🔍 Key Endpoints

/users/register: User registration
/users/token: User authentication
/restaurants/: Restaurant management
/orders/: Order processing

---

## 🙌 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

