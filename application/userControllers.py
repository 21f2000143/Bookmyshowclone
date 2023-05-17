from flask import render_template, request, redirect, url_for, session
from flask import current_app as app
import string
from .database import db
from .models import *
from datetime import datetime
import os
import numbers
# user login
@app.route('/ts/user/login', methods=['GET'])
def user_login():
    return render_template('userlogin.html')

# User validation  
@app.route('/ts/user/validation', methods=['POST', 'GET'])
def user_validation():
    if request.method=='POST':
        admin_login_status='success_user'
        userid = request.form['Email']
        if userid is not None:
            pasw = request.form['password']
            if pasw is not None:
                if "@" not in userid:
                    admin_login_status='invalid_email_user'
                    return render_template('adminpage.html', admin_login_status=admin_login_status)            
                user = User.query.filter_by(user_id=userid).first()
                if user is not None:
                    if user.user_id==userid:
                        if user.user_pass==pasw:
                            session['username']=userid
                            app.logger.debug("User login successfully!")
                            app.logger.error("User login successfully!")
                            # for debugging use pdb module!
                            # import pdb; pdb.set_trace()
                            return render_template('adminpage.html', admin_login_status=admin_login_status, userid=userid)
                        else:
                            admin_login_status='incorrect_password_user'
                            return render_template('adminpage.html', admin_login_status=admin_login_status)
                    else:
                        admin_login_status='no_user_found'
                        return render_template('adminpage.html', admin_login_status=admin_login_status)
                else:
                    admin_login_status='no_user_found'
                    return render_template('adminpage.html', admin_login_status=admin_login_status)
            else:
                admin_login_status='empty_user'
                return render_template('adminpage.html',)
        else:
            admin_login_status='empty_user'
            return render_template('adminpage.html',)
    if request.method=='GET':
        if 'username' in session:
            admin_login_status='success_user'
            return render_template('adminpage.html', admin_login_status=admin_login_status, userid=session['username'])
        return redirect(url_for('user_login'))
     
# User dashboard
@app.route('/ts/user/dashboard/<string:userid>', methods=['POST','GET'])
def user_dashboard(userid):
    if 'username' in session:
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
                    elif isinstance(float(word), numbers.Number):
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
            user = User.query.filter_by(user_id=userid).first()
            i=userid.index("@")
            userid=userid[:i]
            return render_template('user.html', user_id=userid, venues=venues, user=user)
        elif request.method=='GET':
            venues = Venue.query.all()
            user = User.query.filter_by(user_id=userid).first()
            i=userid.index("@")
            userid=userid[:i]
            return render_template('user.html', user_id=userid, venues=venues, user=user)
    else:
        return redirect(url_for('user_login'))

@app.route('/ts/user/user_booking/<string:userid>', methods=['POST','GET'])
def user_booking(userid):
    if 'username' in session:
        user = User.query.filter_by(user_id=userid).first()
        shows=[]
        venues=[]
        for ticket in user.tickets:
            shows+=Show.query.filter_by(show_id=ticket.show_id).with_entities(Show.show_id, Show.show_name, Show.show_stime, Show.show_etime).all()
            venues+=Venue.query.filter_by(venue_id=ticket.venue_id).with_entities(Venue.venue_name).all()            
        user_id=user.user_id
        i=user_id.index("@")
        user_id=user_id[:i]
        return render_template('mybookings.html', user_id=user_id, user=user, shows=shows, venues=venues, limit=len(shows))
    else:
        return redirect(url_for('user_login'))

@app.route('/ts/user/book/<int:show_id>/<string:user_id>/<int:venue_id>', methods=['POST','GET'])
def user_book(show_id, user_id, venue_id):
    if 'username' in session:
        user=User.query.filter_by(user_id=user_id).first()
        venue=Venue.query.filter_by(venue_id=venue_id).first()
        show=Show.query.filter_by(show_id=show_id).first()
        i=user_id.index("@")
        user_id=user_id[:i]
        return render_template('book.html', user_id=user_id, show=show, user=user, venue=venue)
    else:
        return redirect(url_for('user_login'))

@app.route('/ts/rate/<int:show_id>/<string:user_id>', methods=['POST','GET'])
def rate_show(show_id, user_id):
    if 'username' in session:
        if request.method=='GET':
            show = Show.query.filter_by(show_id=show_id).first()
            return render_template('rate.html', show=show, user_id=user_id)
        if request.method=='POST':
            rate=request.form['rate']
            if int(rate)>=0 and int(rate)<=5:
                show = Show.query.filter_by(show_id=show_id).first()
                show.show_rating=float(rate)
                db.session.commit()
                admin_login_status='success_rate'
                return render_template('adminpage.html', admin_login_status=admin_login_status, userid=user_id)
            else:
                admin_login_status='rate_incorrect'
                return render_template('adminpage.html', admin_login_status=admin_login_status, userid=user_id, show_id=show_id)
    else:
        return redirect(url_for('user_login'))


@app.route('/ts/show/booking/<string:user_id>/<int:show_id>/<int:venue_id>', methods=['POST', 'GET'])
def show_book(user_id, show_id, venue_id):
    if 'username' in session:
        show=Show.query.filter_by(show_id=show_id).first()
        number=request.form['Number']
        if show.no_seats>=int(number):
            user=User.query.filter_by(user_id=user_id).first()
            venue=Venue.query.filter_by(venue_id=venue_id).first()
            ticket=Ticket(show_id=show.show_id, venue_id=venue.venue_id, no_seats=number)
            show.no_seats=show.no_seats - int(number)
            user.tickets.append(ticket)
            db.session.commit()
            admin_login_status='success_booked'
            return render_template('adminpage.html', admin_login_status=admin_login_status, userid=user_id)
        else:
            admin_login_status='success_booked_failed'
            return render_template('adminpage.html', admin_login_status=admin_login_status, user_id=user_id, show_id=show_id, venue_id=venue_id)
    else:
        return redirect(url_for('user_login'))

# User account create
@app.route('/ts/user/create', methods=['POST','GET'])
def user_create():
    if request.method=='GET':
        return render_template('create.html')
    elif request.method=='POST':
        email=request.form['Email']
        name=request.form['Name']
        mobile=request.form['mobile']
        password=request.form['password']
        cpassword=request.form['cpassword']
        if email and name and mobile and password:
            if "@" in email:  
                if (name.replace(' ','')).isalpha():
                    if mobile.isdigit():
                        if password==cpassword:
                            user = User(user_id=email, user_name=name, user_mobile=mobile, user_pass=password)
                            db.session.add(user)
                            db.session.commit()
                            user = User.query.first()
                            admin_login_status='user_create_success'
                            session['username']=user.user_id
                            return render_template('adminpage.html', admin_login_status=admin_login_status, userid=email)
                        else:
                            admin_login_status='user_pass_mis'
                            return render_template('adminpage.html', admin_login_status=admin_login_status)
                    else:
                        admin_login_status='invalid_user_mobile'
                        return render_template('adminpage.html', admin_login_status=admin_login_status)
                else:
                    admin_login_status='invalid_user_name'
                    return render_template('adminpage.html', admin_login_status=admin_login_status)
            else:
                admin_login_status='invalid_email_user_create'
                return render_template('adminpage.html', admin_login_status=admin_login_status)
        else:
            admin_login_status='empty_user_create'
            return render_template('adminpage.html',)

@app.route('/logout/user')
def logout_user():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('user_login'))
# ******* User's routers end here ******