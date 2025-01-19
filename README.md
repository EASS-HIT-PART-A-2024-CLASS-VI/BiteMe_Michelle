# 🍔BiteMe: Food Ordering System
This repository contains the code for a Food Ordering System that allows users to order food online, manage menu items, and handle food orders efficiently. The backend is built using FastAPI and follows SOLID principles for clean and modular design.
![_png biteme logo (1)](https://github.com/user-attachments/assets/f7eed7ed-b51a-4a71-8b0e-5cec53db5d64)

---

## 🚀 Features

### Currently Available:
#### Backend:
- 🛒 Order Management: Create, view, and manage food orders.
- 📋 Menu Management: Add, update, and delete menu items.
- 🧬 Testing: Unit and integration tests to ensure the backend works as expected.
- 🐋 Docker Support: Ready for containerization with Docker for easy deployment.

### To Be Continued (Frontend & More):
#### Frontend:
- 🌐 User Interface: A clean and responsive web interface for placing orders and managing the menu.
- 🕱️ User Authentication: Secure login and registration features.
- 🍽️ Order Placement: Users can browse the menu, select items, and place orders.
- 📦 Order Tracking: A system to track the status of placed orders in real-time.
- 💬 User Feedback: Allow users to leave reviews and ratings for the menu items.

---

## 🛠️ Technologies Used

### Backend:
- 🌐 FastAPI: Modern, high-performance web framework for APIs.
- ⚡ Uvicorn: Blazing-fast ASGI server for serving the app.
- ✅ Pydantic: Simplifies data validation and settings management.
- 🐋 Docker: Containerization for portability and scalability.
- 🧬 pytest: Unit and integration testing framework.

### Frontend (To Be Continued):
- React: JavaScript library for building user interfaces.
- Redux: State management for frontend applications.
- Axios: Promise-based HTTP client for making API requests.

---

## 📂 Project Structure

```plaintext
.
├── backend
│   ├── app
│   │   ├── __init__.py         # Package initializer
│   │   ├── crud.py             # Database operations
│   │   ├── database.py         # Database connection setup
│   │   ├── main.py             # FastAPI application entry point
│   │   ├── models.py           # Database models
│   │   ├── schemas.py          # Pydantic schemas for validation
│   │   ├── unit_tests.py       # Unit tests for API endpoints
│   │   └── requirements.txt    # Python dependencies
│   ├── Dockerfile              # Docker configuration
│   ├── integration_test.py     # Integration tests for the app
│   └── requirements.txt        # Project-wide dependencies
├── README.md                   # Project documentation
```

---

## **👄 Installation**

### Prerequisites
Ensure Python 3.9+ is installed. Download it [here](https://www.python.org/downloads/).

### Steps

1. **Clone the Repository:**
```
git clone https://github.com/EASS-HIT-PART-A-2024-CLASS-VI/BiteMe.git
cd BiteMe
   ```

3. **Create a Virtual Environment:**
```
python3 -m venv venv
 ```

3. **Activate the Virtual Environment:**
   - **Windows:**
    ```
     .\venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```
     source venv/bin/activate
     ```

4. **Install Dependencies:**
   ```
   pip install -r backend/app/requirements.txt
   ```

---

## ▶️ **Running the Application**

Start the FastAPI application:

```
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

Visit the app at [http://localhost:8000](http://localhost:8000).

---

## **🧬 Running Tests**

Run unit and integration tests:
```
pytest
```

---

## **🐋 Docker Support**

1. **Build the Docker Image:**
 ```
docker build -t food-ordering-backend .
   ```
2. **Run the Docker Container:**
```
docker run -d -p 8000:8000 food-ordering-backend
   ```

Access the app at [http://localhost:8000](http://localhost:8000).

---

## 🙌 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

