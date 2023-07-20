from flask import render_template, redirect, url_for, request
from flask import current_app as app
from flask_security import current_user, login_required
from application.database import db
from application import tasks
from .models import *
from flask_security import roles_required
import numbers
from datetime import datetime
from flask_sse import sse



# User dashboard
@app.route('/', methods=['GET','POST'])
def welcome():
    if request.method=='POST':
        wor=request.form['words']
        wor=wor.split(',')
        words=[x.strip() for x in wor]
        # five parameters for searching in user dashboard!
        venue_name=Venue.query.with_entities(Venue.venue_name).all()
        vname=[tup[0].upper() for tup in venue_name]
        venue_place=Venue.query.with_entities(Venue.venue_place).all()
        vplace=[tup[0].upper() for tup in venue_place]
        show_name=Show.query.with_entities(Show.show_name).all()
        sname=[tup[0].upper() for tup in show_name]
        show_rating=Show.query.with_entities(Show.show_rating).all()
        srating=[tup[0] for tup in show_rating]
        show_tag=Show.query.with_entities(Show.show_tag).all()
        stag=[tup[0].upper() for tup in show_tag]

        primarykeys=[]
        for word in words:
            if primarykeys==[]:
                if word.upper() in vname:
                    primarykey=Venue.query.filter(Venue.venue_name.ilike('%'+word+'%')).with_entities(Venue.venue_id).all()
                    primarykeys=[tup[0] for tup in primarykey]
                elif word.upper() in vplace:
                    primarykey=Venue.query.filter(Venue.venue_place.ilike('%'+word+'%')).with_entities(Venue.venue_id).all()
                    primarykeys=[tup[0] for tup in primarykey]
                elif word.upper() in sname:
                    primarykey=Show.query.filter(Show.show_name.ilike('%'+word+'%')).with_entities(Show.show_id).all()
                    primarykey1=[tup[0] for tup in primarykey]
                    venue_shows=Venue_Shows.query.all()
                    for vs in venue_shows:
                        if vs.show_id in primarykey1:
                            if vs.venue_id not in primarykeys:
                                primarykeys.append(vs.venue_id)
                elif isinstance(word, numbers.Number):
                    if float(word) in srating:
                        primarykey=Show.query.filter_by(show_rating=float(word)).with_entities(Show.show_id).all()
                        primarykey1=[tup[0] for tup in primarykey]
                        venue_shows=Venue_Shows.query.all()
                        for vs in venue_shows:
                            if vs.show_id in primarykey1:
                                if vs.venue_id not in primarykeys:
                                    primarykeys.append(vs.venue_id)
                    else:
                        pass
                elif word.upper() in stag:
                    primarykey=Show.query.filter(Show.show_tag.ilike('%'+word+'%')).with_entities(Show.show_id).all()
                    primarykey1=[tup[0] for tup in primarykey]
                    venue_shows=Venue_Shows.query.all()
                    for vs in venue_shows:
                        if vs.show_id in primarykey1:
                            if vs.venue_id not in primarykeys:
                                primarykeys.append(vs.venue_id)
                else:
                    pass
            else:
                midprimarykey=[]
                if word in vname:
                    primarykey=Venue.query.filter(Venue.venue_name.ilike('%'+word+'%')).with_entities(Venue.venue_id).all()
                    midprimarykey=[tup[0] for tup in primarykey]
                elif word in vplace:
                    primarykey=Venue.query.filter(Venue.venue_place.ilike('%'+word+'%')).with_entities(Venue.venue_id).all()
                    midprimarykey=[tup[0] for tup in primarykey]
                elif word in sname:
                    primarykey=Show.query.filter(Show.show_name.ilike('%'+word+'%')).with_entities(Show.show_id).all()
                    primarykey1=[tup[0] for tup in primarykey]
                    venue_shows=Venue_Shows.query.all()
                    for vs in venue_shows:
                        if vs.show_id in primarykey1:
                            if vs.venue_id not in primarykeys:
                                primarykeys.append(vs.venue_id)
                elif word in srating:
                    primarykey=Show.query.filter_by(show_rating=float(word)).with_entities(Show.show_id).all()
                    primarykey1=[tup[0] for tup in primarykey]
                    venue_shows=Venue_Shows.query.all()
                    for vs in venue_shows:
                        if vs.show_id in primarykey1:
                            if vs.venue_id not in midprimarykey:
                                midprimarykey.append(vs.venue_id)
                elif word in stag:
                    primarykey=Show.query.filter(Show.show_tag.ilike('%'+word+'%')).with_entities(Show.show_id).all()
                    primarykey1=[tup[0] for tup in primarykey]
                    venue_shows=Venue_Shows.query.all()
                    for vs in venue_shows:
                        if vs.show_id in primarykey1:
                            if vs.venue_id not in midprimarykey:
                                midprimarykey.append(vs.venue_id)
                else:
                    pass
                if midprimarykey!=[]:
                    set1=set(primarykeys)
                    set2=set(midprimarykey)
                    primarykeys=list(set1.intersection(set2))
        venues = []
        for pkey in primarykeys:
            venues.append(Venue.query.filter_by(venue_id=pkey).first())
        seats = Seats.query.all()
        return render_template('welcome.html', venues=venues, seats=seats)
    elif request.method=='GET':
        venues = Venue.query.all()
        seats = Seats.query.all()
        return render_template('welcome.html', venues=venues, seats=seats)

@app.route('/theatre/<int:vid>', methods=['POST', 'GET'])
def theatre_view(vid):
    venues = Venue.query.filter_by(venue_id=vid).first()
    seats = Seats.query.filter_by(venue_id=vid).all()
    print(seats)
    return render_template('venueview.html', venues=venues, seats=seats)

@app.route('/redirecting', methods=['GET', 'POST'])
@login_required
def redirecting():
    if current_user.has_role('admin'):
        return redirect(url_for('admin_dashboard'))
    elif current_user.has_role('user'):
        user=User.query.filter_by(id=current_user.id).first()
        user.last_login_at=datetime.now()
        db.session.commit()
        return redirect(url_for('user_dashboard'))
    else:
        role = Role.query.filter_by(name='user').first()
        app.security.datastore.add_role_to_user(user=current_user, role=role)
        db.session.commit()
        return redirect(url_for('user_dashboard'))
#------------------------------celery tasks endpoints----------------------------#
# @app.route('/hello/<string:user_name>', methods=['POST', 'GET'])
# def just_say_hello(user_name):
#     job = tasks.just_say_hello.delay(user_name)
#     result=job.wait()
#     return str(result), 200

# @app.route('/hello/time', methods=['POST', 'GET'])
# def print_current_time_job():
#     print("IN flask app")
#     now = datetime.now()
#     print("now =", now)
#     dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#     job = tasks.print_current_time_job.apply_async(countdown=10)
#     result=job.wait()
#     return str(result), 200

# @app.route('/show_updates', methods=['GET'])
# def show_updates():
#     return render_template('show_updates.html', error=None)

# @app.route('/email_sending', methods=['GET'])
# def email_sending():
#     job = tasks.send_daily_reminder.delay()
#     result=job.wait()
#     return str(result), 200

# @app.route('/show_updates_vue', methods=['GET'])
# def show_updates_vue():
#     return render_template('show_updates_vue.html', error=None)

# @app.route('/test_send_message', methods=['GET'])
# def test_send_message():
#     sse.publish({"message": "hello!"}, type='greeting')
#     return "Message sent to browsers, please check!"

# @app.route("/start_long_running_job", methods=["GET","POST"])
# def start_long_running_job():
#     job_id = tasks.long_running_job.delay()
#     sse.publish({"message": "STARTING JOB "+ str(job_id)}, type='greeting')
#     return "STARTED!"+str(job_id)
# @app.route('/test/vue')
# def vuetest():
#     return render_template('alertmessage.html')