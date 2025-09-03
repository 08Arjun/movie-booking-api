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


git clone https://github.com/08Arjun/movie-booking-api.git
cd movie-booking-api
### 2. Create virtual environment & activate 
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate # On Mac/Linux
### 3. Install dependencies
pip install -r requirements.txt
### 4. Configure Database
DATABASE_URL = "mysql+pymysql://root:Pathak%402212@localhost/movie_booking"
### 5. Run the app
uvicorn main:app --reload

