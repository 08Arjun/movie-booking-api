from sqlalchemy.orm import Session
import models, schemas
import json
from sqlalchemy import and_
from datetime import datetime

# ---------------- MOVIES ----------------
def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def get_movies(db: Session):
    return db.query(models.Movie).all()


# ---------------- THEATERS ----------------
def create_theater(db: Session, theater: schemas.TheaterCreate):
    db_theater = models.Theater(**theater.dict())
    db.add(db_theater)
    db.commit()
    db.refresh(db_theater)
    return db_theater

def get_theaters(db: Session):
    return db.query(models.Theater).all()


# ---------------- HALLS ----------------
def create_hall(db: Session, hall: schemas.HallCreate):
    hall_dict = hall.dict()
    # Convert rows_layout to JSON string for DB
    hall_dict["rows_layout"] = json.dumps(hall_dict["rows_layout"])
    db_hall = models.Hall(**hall_dict)
    db.add(db_hall)
    db.commit()
    db.refresh(db_hall)
    return db_hall

def get_halls(db: Session):
    halls = db.query(models.Hall).all()
    # Convert rows_layout JSON string back to list
    for h in halls:
        if isinstance(h.rows_layout, str):
            h.rows_layout = json.loads(h.rows_layout)
    return halls


# ---------------- SHOWS ----------------
def create_show(db: Session, show: schemas.ShowCreate):
    db_show = models.Show(**show.dict())
    db.add(db_show)
    db.commit()
    db.refresh(db_show)
    return db_show

def get_shows(db: Session):
    return db.query(models.Show).all()


# ---------------- SEATS ----------------
def create_seats_for_show(db: Session, show_id: int, layout_json: list[dict]):
    seats = []
    for row in layout_json:
        for number in range(1, row["seats"] + 1):
            seats.append(models.Seat(show_id=show_id, row=row["row"], number=number))
    db.bulk_save_objects(seats)
    db.commit()
    return seats

def get_seats(db: Session, show_id: int):
    return db.query(models.Seat).filter(models.Seat.show_id == show_id).all()


# ---------------- BOOKINGS ----------------
def book_seats(db: Session, show_id: int, seat_ids: list[int], user_group: str):
    seats = db.query(models.Seat).filter(
        and_(models.Seat.show_id == show_id, models.Seat.id.in_(seat_ids))
    ).with_for_update().all()

    for seat in seats:
        if seat.booked:
            return None

    for seat in seats:
        seat.booked = True

    booking = models.Booking(
        show_id=show_id,
        seat_ids=",".join([str(s.id) for s in seats]),
        user_group=user_group
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


# ---------------- GROUP BOOKINGS ----------------
def group_book_seats(db: Session, show_id: int, group_size: int, user_group: str):
    seats = db.query(models.Seat).filter(
        models.Seat.show_id == show_id, models.Seat.booked == False
    ).order_by(models.Seat.row, models.Seat.number).all()

    # Map seats by row
    row_map = {}
    for seat in seats:
        row_map.setdefault(seat.row, []).append(seat)

    for row_seats in row_map.values():
        for i in range(len(row_seats) - group_size + 1):
            segment = row_seats[i:i+group_size]
            if all(segment[j].number == segment[0].number + j for j in range(group_size)):
                # Book seats
                for s in segment:
                    s.booked = True
                booking = models.Booking(
                    show_id=show_id,
                    seat_ids=",".join(str(s.id) for s in segment),
                    user_group=user_group
                )
                db.add(booking)
                db.commit()
                db.refresh(booking)
                return {"success": True, "booking": booking, "suggestions": None}

    # Suggest other shows if not enough seats
    show = db.query(models.Show).filter(models.Show.id == show_id).first()
    other_shows = db.query(models.Show).filter(
        models.Show.movie_id == show.movie_id,
        models.Show.hall_id == show.hall_id,
        models.Show.id != show_id
    ).all()

    suggestions = []
    for s in other_shows:
        available_seats = db.query(models.Seat).filter(
            models.Seat.show_id == s.id,
            models.Seat.booked == False
        ).count()
        if available_seats >= group_size:
            suggestions.append({"show_id": s.id, "available_seats": available_seats})

    return {"success": False, "booking": None, "suggestions": suggestions}


# ---------------- ANALYTICS ----------------
def get_movie_analytics(db: Session, movie_id: int, start_date: datetime = None, end_date: datetime = None):
    query = db.query(models.Booking, models.Show).join(
        models.Show, models.Booking.show_id == models.Show.id
    ).filter(models.Show.movie_id == movie_id)

    if start_date:
        query = query.filter(models.Show.start_time >= start_date)
    if end_date:
        query = query.filter(models.Show.start_time <= end_date)

    bookings = query.all()
    total_tickets = 0
    total_gmv = 0.0
    for booking, show in bookings:
        seat_count = len(booking.seat_ids.split(","))
        total_tickets += seat_count
        total_gmv += seat_count * show.price
    return {"total_tickets": total_tickets, "total_gmv": total_gmv}
