from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "testdb.sqlite3")

engine = create_engine(SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import application.models
    Base.metadata.create_all(bind=engine)
# from sqlalchemy.ext.declarative import declarative_base
# from flask_sqlalchemy import SQLAlchemy

# engine = None
# Base = declarative_base()
# db = SQLAlchemy()

# # def db_init(app):
# #     db.init_app(app)

# #     # Creates the tables if the db doesn't already exist
# #     with app.app_context():
# #         db.create_all()