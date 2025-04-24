# plpdb_week8assgnment
# 📚 FastAPI Library Management System

This is a simple **Library Management API** built using **FastAPI** and **SQLAlchemy**, with support for JWT-based authentication, book lending and returns, and fines for overdue returns.

---

## 🚀 Features

- ✅ JWT Authentication (Login required for most routes)
- 📘 Book Lending & Returning
- ⏰ Automatic fines for overdue books
- 🔍 Fetch personal loan records
- 📊 Swagger UI documentation
- 🔐 Secure routes with token-based auth

---

## 📦 Tech Stack

- **FastAPI** – Web framework
- **SQLAlchemy** – ORM / direct SQL execution
- **MariaDB/MySQL** – Relational database
- **JWT** – Authentication via tokens
- **Pydantic** – Data validation & schemas

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/your-username/library-system-api.git
cd library-system-api

# Create and activate a virtual environment
python3 -m venv .wenv
source .wenv/bin/activate

# Install dependencies
pip install -r requirements.txt

#configuration
DATABASE_URI = "mysql+pymysql://username:password@localhost:3306/library"
SECRET_KEY = "your_super_secret"
ALGORITHM = "HS256"

uvicorn app.main:app --reload

#Here are screenhosts of the API in action
![My Loans Response](screenhosts/'Screenshot 2025-04-24 223208.png')
