from flask import render_template, request
from flask import current_app as app
from application.database import db
from .models import *
from datetime import datetime
import numbers
from flask_security import login_required, current_user, roles_required

     
# User dashboard
@app.route('/user/dashboard', methods=['POST','GET'])
@login_required
@roles_required('user')
def user_dashboard():
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
        email = current_user.email
        i=email.index("@")
        email=email[:i]
        
        return render_template('user.html', venues=venues, user=email, current_user=current_user)
    elif request.method=='GET':
        venues = Venue.query.all()
        seats=Seats.query.all()
        email = current_user.email
        i=email.index("@")
        email=email[:i]
        return render_template('user.html', venues=venues, user=email, seats=seats, current_user=current_user)

@app.route('/user/user_booking', methods=['POST','GET'])
@login_required
@roles_required('user')
def user_booking():
    shows=[]
    venues=[]
    for ticket in current_user.tickets:
        shows+=Show.query.filter_by(show_id=ticket.show_id).with_entities(Show.show_id, Show.show_name, Show.show_stime, Show.show_etime).all()
        venues+=Venue.query.filter_by(venue_id=ticket.venue_id).with_entities(Venue.venue_name).all()            
    email=current_user.email
    i=email.index("@")
    email=email[:i]
    return render_template('mybookings.html', user=email, shows=shows, venues=venues, limit=len(shows))

@app.route('/user/book/<int:show_id>/<int:venue_id>', methods=['POST','GET'])
@login_required
@roles_required('user')
def user_book(show_id, venue_id):
    email=current_user.email
    venue=Venue.query.filter_by(venue_id=venue_id).first()
    show=Show.query.filter_by(show_id=show_id).first()
    seat=Seats.query.filter_by(venue_id=venue.venue_id, show_id=show.show_id, book_time=datetime.now()).first()
    i=email.index("@")
    email=email[:i]
    return render_template('book.html', show=show, user=email, venue=venue, seat=seat)

@app.route('/ts/rate/<int:show_id>', methods=['POST','GET'])
@login_required
@roles_required('user')
def rate_show(show_id):
    if request.method=='GET':
        show = Show.query.filter_by(show_id=show_id).first()
        return render_template('rate.html', show=show)
    if request.method=='POST':
        rate=request.form['rate']
        if int(rate)>=0 and int(rate)<=5:
            show = Show.query.filter_by(show_id=show_id).first()
            show.show_rating=float(rate)
            db.session.commit()
            admin_login_status='success_rate'
            return render_template('adminpage.html', admin_login_status=admin_login_status)
        else:
            admin_login_status='rate_incorrect'
            return render_template('adminpage.html', admin_login_status=admin_login_status, show_id=show_id)


@app.route('/ts/show/booking/<int:show_id>/<int:venue_id>', methods=['POST', 'GET'])
@login_required
@roles_required('user')
def show_book(show_id, venue_id):
    seat=Seats.query.filter_by(show_id=show_id, venue_id=venue_id).first()
    number=request.form['Number']
    if seat.no_seats>=int(number):
        user=User.query.filter_by(id=current_user.id).first()
        venue=Venue.query.filter_by(venue_id=venue_id).first()
        ticket=Ticket(show_id=seat.show_id, venue_id=venue.venue_id, no_seats=number)
        seat.no_seats=seat.no_seats - int(number)
        user.tickets.append(ticket)
        db.session.commit()
        admin_login_status='success_booked'
        return render_template('adminpage.html', admin_login_status=admin_login_status)
    else:
        admin_login_status='success_booked_failed'
        return render_template('adminpage.html', admin_login_status=admin_login_status, show_id=show_id, venue_id=venue_id)

#User account create
@app.route('/user/create', methods=['POST','GET'])
@login_required
@roles_required('user')
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
                            user = User(email=email, user_name=name, user_mobile=mobile, user_pass=password)
                            db.session.add(user)
                            db.session.commit()
                            admin_login_status='user_create_success'
                            return render_template('adminpage.html', admin_login_status=admin_login_status, userid=current_user.email)
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
            return render_template('adminpage.html')

@app.route('/user/theatre/<int:vid>')
@login_required
def utheatre_view(vid):
    venues = Venue.query.filter_by(venue_id=vid).first()
    seats = Seats.query.filter_by(venue_id=vid).all()
    return render_template('uvenueview.html', venues=venues, user=current_user, seats=seats)
# ******* User's routers end here ******