from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

import models, schemas, crud
from database import engine, get_db, Base

# Create all tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Ticket Booking API")

# ---------------- MOVIES ----------------
@app.post("/movies/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    return crud.create_movie(db, movie)

@app.get("/movies/", response_model=List[schemas.Movie])
def get_movies(db: Session = Depends(get_db)):
    return crud.get_movies(db)

# ---------------- THEATERS ----------------
@app.post("/theaters/", response_model=schemas.Theater)
def create_theater(theater: schemas.TheaterCreate, db: Session = Depends(get_db)):
    return crud.create_theater(db, theater)

@app.get("/theaters/", response_model=List[schemas.Theater])
def get_theaters(db: Session = Depends(get_db)):
    return crud.get_theaters(db)

# ---------------- HALLS ----------------
@app.post("/halls/", response_model=schemas.Hall)
def create_hall(hall: schemas.HallCreate, db: Session = Depends(get_db)):
    return crud.create_hall(db, hall)

@app.get("/halls/", response_model=List[schemas.Hall])
def get_halls(db: Session = Depends(get_db)):
    return crud.get_halls(db)

# ---------------- SHOWS ----------------
@app.post("/shows/", response_model=schemas.Show)
def create_show(show: schemas.ShowCreate, db: Session = Depends(get_db)):
    return crud.create_show(db, show)

@app.get("/shows/", response_model=List[schemas.Show])
def get_shows(db: Session = Depends(get_db)):
    return crud.get_shows(db)

# ---------------- SEATS ----------------
@app.post("/shows/{show_id}/seats/", response_model=List[schemas.Seat])
def create_seats(show_id: int, seat_layout: schemas.SeatLayout, db: Session = Depends(get_db)):
    return crud.create_seats_for_show(db, show_id, seat_layout.rows_layout)

@app.get("/shows/{show_id}/seats/", response_model=List[schemas.Seat])
def get_seats(show_id: int, db: Session = Depends(get_db)):
    return crud.get_seats(db, show_id)

# ---------------- BOOKINGS ----------------
@app.post("/bookings/", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    db_booking = crud.book_seats(db, booking.show_id, booking.seat_ids, booking.user_group)
    if not db_booking:
        raise HTTPException(status_code=400, detail="One or more seats already booked")
    return db_booking

@app.get("/bookings/", response_model=List[schemas.Booking])
def get_bookings(db: Session = Depends(get_db)):
    return crud.get_bookings(db)

# ---------------- GROUP BOOKING ----------------
@app.post("/group-booking/", response_model=schemas.GroupBookingResponse)
def group_booking(req: schemas.GroupBookingRequest, db: Session = Depends(get_db)):
    return crud.group_book_seats(db, req.show_id, req.group_size, req.user_group)

# ---------------- ANALYTICS ----------------
@app.get("/analytics/movies/{movie_id}")
def movie_analytics(movie_id: int, start_date: datetime = None, end_date: datetime = None, db: Session = Depends(get_db)):
    return crud.get_movie_analytics(db, movie_id, start_date, end_date)
