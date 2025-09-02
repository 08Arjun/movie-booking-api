from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import json

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    duration = Column(Integer)
    genre = Column(String(50))
    price = Column(Float)
    release_date = Column(DateTime)
    shows = relationship("Show", back_populates="movie")

class Theater(Base):
    __tablename__ = "theaters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(200))
    halls = relationship("Hall", back_populates="theater")

class Hall(Base):
    __tablename__ = "halls"
    id = Column(Integer, primary_key=True, index=True)
    theater_id = Column(Integer, ForeignKey("theaters.id"))
    name = Column(String(50))
    rows_layout = Column(String(500))  # JSON stored as string
    theater = relationship("Theater", back_populates="halls")
    shows = relationship("Show", back_populates="hall")

    @property
    def rows_layout_json(self):
        return json.loads(self.rows_layout) if self.rows_layout else []

    @rows_layout_json.setter
    def rows_layout_json(self, value):
        self.rows_layout = json.dumps(value)

class Show(Base):
    __tablename__ = "shows"
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    hall_id = Column(Integer, ForeignKey("halls.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    price = Column(Float)
    movie = relationship("Movie", back_populates="shows")
    hall = relationship("Hall", back_populates="shows")
    seats = relationship("Seat", back_populates="show")

class Seat(Base):
    __tablename__ = "seats"
    id = Column(Integer, primary_key=True, index=True)
    show_id = Column(Integer, ForeignKey("shows.id"))
    row = Column(Integer)
    number = Column(Integer)
    booked = Column(Boolean, default=False)
    show = relationship("Show", back_populates="seats")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    show_id = Column(Integer, ForeignKey("shows.id"))
    user_group = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    seat_ids = Column(String(200))
    show = relationship("Show")
