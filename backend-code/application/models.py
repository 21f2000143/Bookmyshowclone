# from .database import db
# from sqlalchemy import Index
# from flask_security import UserMixin, RoleMixin

from application.database import *
from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                    String, ForeignKey, UnicodeText, Float

#Creating models/tables for the the database
class Venue(db.Model):
    __tablename__= 'venue'
    venue_id=Column(Integer, primary_key=True, autoincrement = True)
    venue_name = Column(String, nullable=False)
    venue_place = Column(String, nullable=False)
    venue_capacity = Column(Integer, nullable=False)
    venue_location = Column(String, nullable=False)
    shows = relationship('Show', secondary='venue_shows')

class Seats(db.Model):
    __tablename__='seats'
    seats_id=Column(Integer, primary_key=True, autoincrement=True)
    venue_id=Column(Integer, nullable=False)
    show_id=Column(Integer, nullable=False)
    no_seats = Column(Integer)

class Show(db.Model):
    __tablename__='show'
    show_id=Column(Integer, primary_key=True, autoincrement=True)
    show_name = Column(String, nullable=False)
    img_name = Column(String)
    show_rating = Column(Float)
    show_tag = Column(String(20), nullable=False)
    show_price = Column(Float, nullable=False)
    show_stime = Column(DateTime)
    show_etime = Column(DateTime)
    # show_venue = Column(String, nullable=False)
    # venue_id=Column(Integer, ForeignKey('venue.venue_id'))
    # user_id=Column(String, ForeignKey('user.user_id'))
    # venues = relationship('Venue', secondary='venue_shows')
    # trailer = Column(Text)
    
# # creating virtual table
# class Search_Show(Model):
#     __tablename__='search_show'
#     rowid=Column(Integer, primary_key=True)
#     show_name=Column(String)
#     show_tag=Column(String)

class Venue_Shows(db.Model):
    __tablename__='venue_shows'
    show_id = Column(Integer, ForeignKey('show.show_id'), primary_key=True, nullable=False)
    venue_id = Column(Integer, ForeignKey('venue.venue_id'), primary_key=True, nullable=False)

# class Slot(Model):
#     __tablename__ = 'slot'
#     slot_id = Column(Integer, primary_key=True, autoincrement = True)
#     slot_stime = Column(DateTime, unique=True)
#     slot_etime = Column(DateTime, unique=True)
#     venues = relationship('Venue', secondary='venue_slots')
#     shows = relationship('Show', secondary='show_slot')

# # class for user using flask-security
# class User(Model, UserMixin):
#     __tablename__ = 'user'
#     id = Column(String, primary_key=True, index=True)
#     user_name = Column(String(20), nullable=False)
#     email = Column(String, unique=True)
#     user_mobile = Column(String(10), nullable=False)
#     password = Column(String(255))
#     active = Column(Boolean())
#     tickets = relationship('Ticket', secondary='user_tickets')
#     fs_uniquifier = Column(String(64), unique=True, nullable=False)
#     role=relationship('Role', secondary=roles_users, backref=backref('users', lazy='dynamic'))

class User_Tickets(db.Model):
    __tablename__='user_tickets'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    ticket_id = Column(Integer, ForeignKey('ticket.ticket_id'), primary_key=True, nullable=False)

# class User(Model):
#     __tablename__ = 'admin'
#     emp_id = Column(String, primary_key=True)
#     emp_name = Column(String(20), nullable=False)
#     emp_mobile = Column(String(20), nullable=False)
#     emp_pass = Column(String, nullable=False) 

class Ticket(db.Model):
    __tablename__='ticket'
    ticket_id = Column(Integer(), primary_key=True, autoincrement=True)
    venue_id = Column(Integer(), nullable=False)
    show_id = Column(Integer(), nullable=False)
    no_seats = Column(Integer(), nullable=False)
    book_time = Column(DateTime)
# All models have been created, let's move to other part.

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(UnicodeText)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    mobile = Column(String(10))
    tickets = relationship('Ticket', secondary='user_tickets')
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))
    