import os
from flask import Flask, render_template, redirect, url_for
from application.config import LocalDevelopmentConfig
from application.database import db_session, init_db
from application.models import *
from flask_restful import Api
from flask_security import Security, current_user, login_required, auth_required, hash_password, SQLAlchemySessionUserDatastore, UserDatastore

from flask_wtf import FlaskForm
from wtforms import SelectField


from wtforms import SelectField
from flask_security.forms import RegisterForm

class ExtendedRegisterForm(RegisterForm):
    role = SelectField('Role', choices=[('admin', 'Admin'), ('user', 'User'), ('superuser', 'Superuser')])

# applying logging in the project
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
import logging

user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)

app, api = None, None
def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development")== "production":
        # app.logger.info("Currently no production is being setup")
        raise Exception("Currently no production config is setup.")
    else:
        print("Started local development")
        # app.logger.info("Starting local development")
        app.config.from_object(LocalDevelopmentConfig)
    # db.init_app(app)
    app.app_context().push()
    # db.create_all()
    api=Api(app)
    app.security = Security(app, user_datastore, register_form=ExtendedRegisterForm)# to pass your user form {register_form=ExtendedRegisterForm}
    with app.app_context():
        # Create a user to test with
        init_db()

        # To initialize the roles in the role table
        roles = [
                ('admin', 'Administrator'),
                ('user', 'User'),
                ('superuser', 'Superuser')
            ]
        for name, description in roles:
            role = Role.query.filter_by(name=name).first()
            if role is None:
                role = Role(name=name, description=description)
                db_session.add(role)
        db_session.commit()
        # To add admin on initializing of database
        role = Role.query.filter_by(name='admin').first()
        if not app.security.datastore.find_user(email="sk9666338@gmail.com"):
            app.security.datastore.create_user(email="sk9666338@gmail.com", password=hash_password("password"))
        db_session.commit()
        user=app.security.datastore.find_user(email="sk9666338@gmail.com")
        app.security.datastore.add_role_to_user(user=user,role=role)
        db_session.commit()
    return app, api

app, api = create_app()


# import all the controllers so they are loaded
app.logger.info("Starting local development")

@app.errorhandler(404)
def page_not_found(e):
    # setting 404 status explicitly
    return render_template('404.html'), 404

from application.adminControllers import *
from application.userControllers import *
from application.welcome import *

from application.api import venueApi, showApi, userApi
api.add_resource(venueApi, '/get/venue', '/get/venue/<int:venue_id>')
api.add_resource(showApi, '/get/show', '/get/show/<int:show_id>')
api.add_resource(userApi, '/get/user', '/get/user/<int:id>')


if __name__=="__main__":
    # Run the Flask app
    app.run(host='0.0.0.0', port=8000)
    