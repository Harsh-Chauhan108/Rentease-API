# 🏠 RentEase API

A production-ready House Rental Backend System built with FastAPI. It provides secure authentication, role-based authorization, property management, and booking APIs using SQLAlchemy ORM and MySQL.

---

## 🚀 Features

- JWT Authentication
- Refresh Token Authentication
- Password Hashing (bcrypt)
- Role-Based Authorization (Owner & Tenant)
- Property CRUD APIs
- Booking APIs
- SQLAlchemy ORM
- MySQL Database
- Middleware Logging
- Rate Limiting (SlowAPI)
- Dependency Injection
- Swagger API Documentation

---

## 🛠️ Tech Stack

- FastAPI
- Python
- SQLAlchemy
- MySQL
- Pydantic
- JWT (python-jose)
- Passlib (bcrypt)
- SlowAPI
- Uvicorn

---

## 📂 Project Structure

```
rentease/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── tokens.py
│   ├── dependencies.py
│   ├── middleware.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── property.py
│   │   └── booking.py
│   └── utils/
│       └── hashing.py
│
├── requirements.txt
└── run.py
```


## 🔐 Authentication APIs

- Register User
- Login
- Refresh Access Token
- Logout

---

## 🏠 Property APIs

- Add Property
- Update Property
- Delete Property
- View All Properties

---

## 📅 Booking APIs

- Create Booking
- My Bookings

---

## 🔒 Security

- JWT Access Token
- Refresh Token
- Password Hashing
- Protected Routes
- Role-Based Authorization
- Rate Limiting

---


## 👨‍💻 Author

**Harsh Chauhan**
