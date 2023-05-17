import os
from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import *
from flask_restful import Api

# applying logging in the project
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
import logging

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
    db.init_app(app)
    api=Api(app)
    app.app_context().push()
    db.create_all()
    return app, api

app, api = create_app()
from logging.handlers import SMTPHandler

mail_handler = SMTPHandler(
    mailhost='smtp.gmail.com',
    fromaddr='iranisundar@gmail.com',
    toaddrs=['sachinthesensitive2@gmail.com'],
    subject='Application Error',
    credentials=('iranisundar@gmail.com', 'Iltfsg1234'),
    secure=()
)
mail_handler.setLevel(logging.ERROR)
mail_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))

if not app.debug:
    app.logger.addHandler(mail_handler)
# import all the controllers so they are loaded
app.logger.info("Starting local development")

from application.adminControllers import *
from application.userControllers import *

from application.api import venueApi, showApi, userApi, adminApi, ticketApi
api.add_resource(venueApi, '/get/venue', '/get/venue/<int:venue_id>')
api.add_resource(showApi, '/get/show', '/get/show/<int:show_id>')
api.add_resource(userApi, '/get/user', '/get/user/<string:user_id>')
api.add_resource(adminApi, '/get/admin', '/get/admin/<string:emp_id>')


if __name__=="__main__":
    # Run the Flask app
    app.run(host='0.0.0.0', port=8000, debug=False)
    