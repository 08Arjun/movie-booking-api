from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# ---------------- MOVIE ----------------
class MovieBase(BaseModel):
    name: str
    duration: int
    genre: Optional[str] = None
    price: float
    release_date: Optional[datetime] = None

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int
    class Config:
        orm_mode = True

# ---------------- THEATER ----------------
class TheaterBase(BaseModel):
    name: str
    location: Optional[str] = None  # Allow None

class TheaterCreate(TheaterBase):
    pass

class Theater(TheaterBase):
    id: int
    class Config:
        orm_mode = True

# ---------------- HALL ----------------
class RowLayout(BaseModel):
    row: int
    seats: int

class HallBase(BaseModel):
    theater_id: int
    name: Optional[str] = None  # Allow None
    rows_layout: List[RowLayout]

class HallCreate(HallBase):
    pass

class Hall(HallBase):
    id: int
    class Config:
        orm_mode = True

# ---------------- SHOW ----------------
class ShowBase(BaseModel):
    movie_id: int
    hall_id: int
    start_time: datetime
    end_time: datetime
    price: float

class ShowCreate(ShowBase):
    pass

class Show(ShowBase):
    id: int
    class Config:
        orm_mode = True

# ---------------- SEAT ----------------
class SeatBase(BaseModel):
    row: int
    number: int

class SeatCreate(SeatBase):
    pass

class Seat(SeatBase):
    id: int
    show_id: int
    booked: bool
    class Config:
        orm_mode = True

# ---------------- BOOKING ----------------
class BookingBase(BaseModel):
    show_id: int
    seat_ids: List[int]
    user_group: Optional[str] = None  # Allow None

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

# ---------------- GROUP BOOKING ----------------
class GroupBookingRequest(BaseModel):
    show_id: int
    group_size: int
    user_group: Optional[str] = None  # Allow None

class GroupBookingResponse(BaseModel):
    success: bool
    booking: Optional[Booking] = None
    suggestions: Optional[List[dict]] = None

# ---------------- SEAT LAYOUT ----------------
class SeatLayoutRow(BaseModel):
    row: int
    seats: int

class SeatLayout(BaseModel):
    rows_layout: List[SeatLayoutRow]
