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
```
#Here are screenhosts of the API in action

![Auth Token](screenshots/Screenshot2025-04-24223208.png)
![Loaned Books](screenshots/Screenshot%202025-04-24%20223502.png)
![Books Available](screenshots/Screenshot%202025-04-24%20223556.png)
![Loan Return](screenshots/Screenshot%202025-04-24%20223827.png)
![Try Borrowing with existing loan](screenshots/Screenshot%202025-04-24%20223947.png)
![My paid & unpaid fines](screenshots/Screenshot%202025-04-24%20224431.png)
![Fine partial payment](screenshots/Screenshot%202025-04-24%20224614.png)
![Full payment](screenshots/Screenshot%202025-04-24%20224632.png)