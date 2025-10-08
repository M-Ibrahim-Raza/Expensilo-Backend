# Expensilo Backend - FastAPI

A **modular and scalable backend** built with **FastAPI**, designed to manage user transactions efficiently.
The project follows a **clean architecture** with separate layers for **database, models, schemas, services, and routers**, ensuring maintainability and extensibility.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [API Endpoints Overview](#api-endpoints-overview)
5. [Project Structure](#project-structure)
6. [Database Design](#database-design)
7. [Setup Instructions](#setup-instructions)
8. [Best Practices Implemented](#best-practices-implemented)
9. [Future Enhancements](#future-enhancements)
10. [License](#license)

---

## Overview

The **Expensilo API** allows users to manage their financial activities — including creating transactions, categorizing expenses, and maintaining user-specific preferences.
The backend is built using **FastAPI** and **SQLAlchemy (ORM)**, providing a high-performance API layer.

**Core Entities:**

* `User` — Represents an application user.
* `Category` — Represents expense/income categories.
* `Transaction` — Defines base transaction templates.
* `UserCategory` — A user’s association with categories.
* `UserTransaction` — User-specific financial records.

---

## Architecture

The system follows a **layered architecture** with clear separation of concerns:

```
└── app/
    ├── db/              # Database setup, session management, base class
    ├── models/          # SQLAlchemy ORM models
    ├── schemas/         # Pydantic schemas for validation and serialization
    ├── services/        # Business logic layer
    ├── routers/         # FastAPI route handlers
    ├── main.py          # FastAPI application entrypoint
```

Each resource (`User`, `Category`, `Transaction`, etc.) has its own modular implementation across `models`, `schemas`, `services`, and `routers`.

---

## Features

* **User Management:** Create, update, delete, and fetch users.
* **Category Management:** Manage global and user-specific categories.
* **Transaction Management:** CRUD operations on user transactions.
* **Association Models:** Handle many-to-many relations (User–Category, User–Transaction).
* **Validation Layer:** Pydantic models ensure request/response validation.
* **Database Layer:** SQLAlchemy ORM with declarative base and scoped sessions.
* **OpenAPI Support:** Auto-generated documentation via FastAPI (`/docs`, `/redoc`).
* **JSON-based Preferences:** Users can store flexible key-value preferences.

---

## API Endpoints Overview

| Module              | Endpoint                                             | Method | Summary                    |
| ------------------- | ---------------------------------------------------- | ------ | -------------------------- |
| **User**            | `/users`                                             | POST   | Create new user            |
|                     | `/users/{user_id}`                                   | GET    | Get user details           |
|                     | `/users/{user_id}`                                   | PUT    | Update existing user       |
|                     | `/users/{user_id}`                                   | DELETE | Delete user                |
| **Category**        | `/category`                                          | GET    | Get all categories         |
|                     | `/category/{category_name}/users`                    | GET    | Get users under a category |
| **UserCategory**    | `/users/{user_id}/category`                          | GET    | Get user’s categories      |
|                     | `/users/{user_id}/category`                          | POST   | Add category to user       |
|                     | `/users/{user_id}/category/{category_name}`          | DELETE | Remove user category       |
| **Transaction**     | `/transaction`                                       | GET    | Get all transactions       |
| **UserTransaction** | `/users/{user_id}/transaction`                       | GET    | Get user transactions      |
|                     | `/users/{user_id}/transaction`                       | POST   | Create user transaction    |
|                     | `/users/{user_id}/transaction/{user_transaction_id}` | PUT    | Update user transaction    |
|                     | `/users/{user_id}/transaction/{user_transaction_id}` | DELETE | Delete user transaction    |

---

## 🗂 Project Structure

```bash
app/
│
├── db/
│   ├── base.py                # Declarative Base for SQLAlchemy models
│   ├── db_setup.py            # Engine, Session, and database lifecycle methods
│   ├── __init__.py            # Exports Base, init_db, get_db, etc.
│
├── models/
│   ├── user.py
│   ├── category.py
│   ├── user_category.py
│   ├── transaction.py
│   ├── user_transaction.py
│   ├── __init__.py            # Aggregates all model imports
│
├── schemas/
│   ├── user.py
│   ├── category.py
│   ├── transaction.py
│   ├── user_transaction.py
│   ├── user_category.py
│
├── services/
│   ├── user_service.py
│   ├── category_service.py
│   ├── transaction_service.py
│   ├── user_transaction_service.py
│
├── routers/
│   ├── user_router.py
│   ├── category_router.py
│   ├── transaction_router.py
│   ├── user_transaction_router.py
│
└── main.py                     # FastAPI app initialization and route registration
```

---

## Database Design

### Entity Relationships

* **User ↔ UserCategory ↔ Category** — Many-to-Many (User can have multiple categories).
* **User ↔ UserTransaction ↔ Transaction** — Many-to-Many (User has many transactions).

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/expense-tracker-backend.git](https://github.com/M-Ibrahim-Raza/Expensilo.git
cd Expensilo
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

```bash
python -m app.db.db_setup
```

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

Access API documentation:

* Swagger UI → `http://127.0.0.1:8000/docs`
* ReDoc → `http://127.0.0.1:8000/redoc`

---

## Best Practices Implemented

### **Project Structure & Code Design**

* **Separation of Concerns:** Dedicated folders for models, schemas, services, and routers.
* **Dependency Injection:** Database sessions injected into routes using `Depends(get_db)`.
* **Single Responsibility Principle (SRP):** Each service handles only one domain responsibility.
* **Reusability:** Shared mixins for CRUD logic and session handling.

### **Database Management**

* SQLAlchemy 2.0 with `DeclarativeBase` for modern ORM syntax.
* Session-safe helpers (`get_db`, `get_db_session`, `add_commit_refresh`).
* Centralized `Base` for model declarations.

### **Validation & Serialization**

* Pydantic models for request/response validation.
* Type-safe and explicit field definitions with docstrings.

### **Error Handling**

* Consistent use of HTTPException and proper status codes.
* Validation error schemas (`HTTPValidationError`).

### **Documentation**

* Fully OpenAPI-compliant.
* Tag-based endpoint grouping (`Users`, `Category`, `Transaction`).

### **Code Quality**

* Follows **PEP8** and **FastAPI best practices**.
* Reusable utilities and mixins instead of repeated CRUD logic.
* Explicit imports with `__all__` for cleaner module exports.

---

## Future Enhancements

* JWT-based authentication system.
* Dockerized deployment setup.

---
