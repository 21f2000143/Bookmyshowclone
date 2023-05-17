from .database import db
from sqlalchemy import Index

#Creating models/tables for the the database
class Venue(db.Model):
    __tablename__= 'venue'
    venue_id=db.Column(db.Integer, primary_key=True, autoincrement = True)
    venue_name = db.Column(db.String, nullable=False)
    venue_place = db.Column(db.String, nullable=False)
    venue_capacity = db.Column(db.Integer, nullable=False)
    venue_location = db.Column(db.String, nullable=False)
    shows = db.relationship('Show', secondary='venue_shows')
    # This for creating index for multiple columns
    __table_args__ = (
        db.Index('venue_lookup', 'venue_name', 'venue_place', 'venue_location', unique=True),
    )

class Show(db.Model):
    __tablename__='show'
    show_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    show_name = db.Column(db.String, nullable=False)
    show_rating = db.Column(db.Float)
    show_tag = db.Column(db.String(20), nullable=False)
    show_price = db.Column(db.Float, nullable=False)
    no_seats = db.Column(db.Integer, nullable=False)
    show_stime = db.Column(db.DateTime)
    show_etime = db.Column(db.DateTime)
    # show_venue = db.Column(db.String, nullable=False)
    # venue_id=db.Column(db.Integer, db.ForeignKey('venue.venue_id'))
    # user_id=db.Column(db.String, db.ForeignKey('user.user_id'))
    # venues = db.relationship('Venue', secondary='venue_shows')
    # trailer = db.Column(db.Text)
    
# creating virtual table
class Search_Show(db.Model):
    __tablename__='search_show'
    rowid=db.Column(db.Integer, primary_key=True)
    show_name=db.Column(db.String)
    show_tag=db.Column(db.String)

class Venue_Shows(db.Model):
    __tablename__='venue_shows'
    show_id = db.Column(db.Integer, db.ForeignKey('show.show_id'), primary_key=True, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.venue_id'), primary_key=True, nullable=False)

# class Slot(db.Model):
#     __tablename__ = 'slot'
#     slot_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
#     slot_stime = db.Column(db.DateTime, unique=True)
#     slot_etime = db.Column(db.DateTime, unique=True)
#     venues = db.relationship('Venue', secondary='venue_slots')
#     shows = db.relationship('Show', secondary='show_slot')

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.String, primary_key=True, index=True)
    user_name = db.Column(db.String(20), nullable=False)
    user_mobile = db.Column(db.String(10), nullable=False)
    user_pass = db.Column(db.String, nullable=False)
    tickets = db.relationship('Ticket', secondary='user_tickets')

class User_Tickets(db.Model):
    __tablename__='user_tickets'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True, nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.ticket_id'), primary_key=True, nullable=False)

class Admin(db.Model):
    __tablename__ = 'admin'
    emp_id = db.Column(db.String, primary_key=True)
    emp_name = db.Column(db.String(20), nullable=False)
    emp_mobile = db.Column(db.String(20), nullable=False)
    emp_pass = db.Column(db.String, nullable=False) 

class Ticket(db.Model):
    __tablename__='ticket'
    ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_id = db.Column(db.Integer, nullable=False)
    show_id = db.Column(db.Integer, nullable=False)
    no_seats = db.Column(db.Integer, nullable=False)

# All models have been created, let's move to other part.
