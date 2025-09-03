# 🎬 Movie Booking API

A FastAPI-based backend for managing movies, theaters, shows, and bookings.

## 🚀 Features
- Add and fetch **Movies**
- Manage **Theaters**
- Schedule **Shows**
- Create and view **Bookings**
- MySQL database integration with SQLAlchemy

## 🛠️ Tech Stack
- **FastAPI** (Backend framework)
- **SQLAlchemy** (ORM)
- **MySQL** (Database)
- **Uvicorn** (ASGI server)

## 📂 Project Structure

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/08Arjun/movie-booking-api.git
cd movie-booking-api
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate # On Mac/Linux
pip install -r requirements.txt
DATABASE_URL = "mysql+pymysql://username:password@localhost/movie_booking"
uvicorn main:app --reload

