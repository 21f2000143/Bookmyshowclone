# Ticket Show V2 Web App Report

## Author:
- **Name:** Sachin Kumar
- **Roll No:** 21f2000143
- **Student Email ID:** <21f2000143@ds.study.iitm.ac.in>
- **LinkedIn Profile:** <https://www.linkedin.com/in/sachin-kumar-9375211a0>
- **Github Profile:** <https://github.com/SentiSachin>
- **Github Profile:** <https://github.com/SentiSachin>
- **About:** Hey there! this is Sachin, a 24 year old web technologies enthusiast. I am also an undergrad student at IIT Madras BS Degree (Programming and Data Science) || Completed my bachelor's in Computer Science and Engineering. Interested in Development, AI, Data Science and Programming.

Apart from these, I am young energetic guy who never settles without discovering anything new each day. I like traveling, listening music, visiting new places.

## Description
The Ticket Show Web App is a web-based application designed to display ticket information to users also **creation**, **deletion**, and **deletion** of venues, show by the User. The purpose of this report is to provide an overview of the app, including its features, functionality, and potential areas for improvement.

## Frameworks used in the project
- ***Flask***:- for backend of the application
- ***VueJS***:- for UI in the frontend of the application
- ***Flask-Restful***:- for API creation and CRUD operations in Venues, Show, Users tables in the backend of the application
## Tools and Technologies
These are tools and technologies to develop Ticket Show Web App. These include:

- ***Bootstrap***:- for styling and aesthetics of the application
- ***Git***:- Used local git repo for version control tool.
- ***requests***:- Requests is a popular Python library used for making HTTP requests to APIs, websites, and other web services.
- ***os***:- for some operation related with files directory in the application
- ***session***:- Flask extension supports Server-side session to our application.
- ***redirect***:-used to redirect a user to another endpoint using a specified URL and assign a specified
status code.
- ***request***:- used to handle HTTP requests and responses.
- ***render_template***:- used to render html templates based on the Jinja2 engine that is found in the
application's templates folder.
- ***matplotlib.pyplot***:- a python module is used to create dynamic trendline graphs based on the
information provided by the user.
- ***Flask-sqlalchemy***:- used to create database schema and tables using SQLAlchemy with Flask by
providing defaults and helpers.

## Database Schema
1. ***Relations:*** There are five tables in the database namely Venue, Show, User, User, Ticket and two association tables one of show and venue that is Venue_Shows and one for user and tickets that is User_Ticket.

## Architecture and Features:
The project code is organised based on its utility in different files. I have named my project ticket-show.
Inside this folder there are four folder including application, db_directory, static, templates and files main.py, .gitignore and requirements.txt.
Images in static folder, templates in template forlder.
Report folder with the report.pdf file, demo video and one instruction.txt file to setup and run this project on windows.
## Routers used in adminControllers
- @app.route('/ts/admin/login', methods=['GET'])
- @app.route('/ts/admin/validation', methods=['POST', 'GET'])
- @app.route('admin/dashboard', methods=['POST','GET'])
- @app.route('admin/home', methods=['POST', 'GET'])
- @app.route('admin/create_venue', methods=['POST', 'GET'])
- @app.route('/admin/update_venue/<int:v_id>', methods=['POST','GET'])
- @app.route('/admin/delete_venue/<int:v_id>', methods=['POST','GET'])
- @app.route('/ts/admin/delete/<int:v_id>', methods=['POST', 'GET'])
- @app.route('/admin/create_show/<int:v_id>', methods=['POST','GET'])
- @app.route('/admin/show/<int:s_id>/<int:v_id>', methods=['POST','GET'])
- @app.route('/logout')

## Routers used in userControllers
- @app.route('/ts/user/login', methods=['GET'])
- @app.route('/ts/user/validation', methods=['POST', 'GET'])
- @app.route('/user/dashboard', methods=['POST','GET'])
- @app.route('/user/user_booking', methods=['POST','GET'])
- @app.route('/user/book/<int:show_id>/<int:venue_id>', methods=['POST','GET'])
- @app.route('/ts/rate/<int:show_id>', methods=['POST','GET'])
- @app.route('/ts/show/booking/<int:show_id>/<int:venue_id>', methods=['POST', 'GET'])
- @app.route('/user/create', methods=['POST','GET'])
- @app.route('/logout/user')

A short demo video link is here [ Video link ](https://drive.google.com/file/d/1FrPEwxDe7Jm2BoIw5DGASIkaPFAYTqnV/view?usp=sharing).