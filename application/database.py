from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

engine = None
Base = declarative_base()
db = SQLAlchemy()

# def db_init(app):
#     db.init_app(app)

#     # Creates the tables if the db doesn't already exist
#     with app.app_context():
#         db.create_all()