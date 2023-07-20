# all necessary required module
from flask import render_template, request
from flask import current_app as app
from flask_security import login_required, current_user, roles_required
from application.database import db
from .models import *
from datetime import datetime
import os
import numbers

# module to print graph
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ******* User's routers start here *******

@app.route('/admin/dashboard', methods=['POST','GET'])
@login_required
@roles_required('admin')
def admin_dashboard():
    if request.method=='POST':
        if request.form['operation']=='create_venue':
            vname=request.form['vname']
            vplace=request.form['vplace']
            vlocation=request.form['vlocation']
            vcapacity=request.form['vcapacity']
            if len(vname)>0 and len(vplace)>0 and len(vlocation)>0 and len(vcapacity)>0:
                if vcapacity.isdigit():
                    venues= Venue.query.all()
                    if vname in [venue.venue_name for venue in venues] and vplace in [venue.venue_place for venue in venues]:
                        admin_login_status='venue_already_exist'
                        return render_template('adminpage.html', admin_login_status=admin_login_status)
                    else:
                        venue=Venue(venue_name=vname, venue_place=vplace, venue_capacity=vcapacity, venue_location=vlocation)
                        db.session.add(venue)
                        db.session.commit()
                        emp_id=current_user.email
                        i=emp_id.index("@")
                        emp_id=emp_id[:i]
                        venues = Venue.query.all()
                        return render_template('admin.html', emp_id=emp_id, venues=venues)
                else:
                    admin_login_status='invalid_data_literal_venue'
                    return render_template('adminpage.html', admin_login_status=admin_login_status)
            else:
                admin_login_status='not_filled_for_venue_create'
                return render_template('adminpage.html', admin_login_status=admin_login_status)
        elif request.form['operation']=='create_show':
            sname=request.form['sname']
            stag=request.form['stag']
            sprice=request.form['sprice']
            sstime=request.form['sstime']
            setime=request.form['setime']
            img_name=request.form['img_name']
            addedvenues=request.form['addedvenues']
            print(addedvenues)
            if len(addedvenues)> 0 and len(sname)>0 and len(stag)>0 and len(sprice)>0 and len(setime)>0 and len(sstime)>0 and len(img_name)>0:
                if stag.isalpha() and sprice.isdigit() and (setime>sstime):
                    date_format="%H:%M"
                    sstime=datetime.strptime(sstime, date_format)
                    setime=datetime.strptime(setime, date_format)
                    show=Show(show_name=sname, show_tag=stag, show_price=sprice, show_stime=sstime, show_etime=setime, img_name=img_name)
                    db.session.add(show)
                    addedvenues=addedvenues.split(',')
                    for venue_name in addedvenues:
                        venue=Venue.query.filter_by(venue_name=venue_name).first()
                        if venue:
                            if sname not in [show.show_name for show in venue.shows]:
                                venue.shows.append(show)
                                seat=Seats(venue_id=venue.venue_id, show_id=show.show_id, no_seats=venue.venue_capacity)
                                db.session.add(seat)
                                db.session.commit() 
                    db.session.commit()
                    emp_id=current_user.email
                    i=emp_id.index("@")
                    emp_id=emp_id[:i]
                    venues = Venue.query.all()
                    return render_template('admin.html', emp_id=emp_id, venues=venues)
                else:
                    admin_login_status='invalid_data_literal_show'
                    return render_template('adminpage.html', admin_login_status=admin_login_status)
            else:
                admin_login_status='not_filled_for_show_create'
                return render_template('adminpage.html', admin_login_status=admin_login_status)
        elif request.form['operation']=='show_delete' :
            v_id=int(request.form['v_id'])
            s_id=int(request.form['s_id'])
            venue = Venue.query.filter_by(venue_id=v_id).first()
            seat=Seats.query.filter_by(venue_id=v_id, show_id=s_id).first()
            print(seat.venue_id, seat.show_id)
            db.session.delete(seat)
            db.session.commit()
            for show in venue.shows:
                if show.show_id==s_id:
                    venue.shows.remove(show)
            db.session.commit()
            venues=Venue.query.all()
            flag=False
            for each_ven in venues:
                if show.show_id in each_ven.shows:
                    flag=True
            if flag:
                db.session.delete(show)
                db.session.commit()
            admin_login_status='deleted_show'
            return render_template('adminpage.html', admin_login_status=admin_login_status)
        elif request.form['operation']=='show_update' :
            v_id=int(request.form['v_id'])
            s_id=int(request.form['s_id'])
            sname=request.form['sname']
            stag=request.form['stag']
            sprice=request.form['sprice']
            sstime=request.form['sstime']
            setime=request.form['setime']
            date_format="%H:%M"
            sstime=datetime.strptime(sstime, date_format)
            setime=datetime.strptime(setime, date_format)
            try:
                venue = Venue.query.filter_by(venue_id=v_id).first()
                this_show=None
                for show in venue.shows:
                    if show.show_id==s_id:
                        this_show=show
                        break
                this_show.show_name=sname
                this_show.show_tag=stag
                this_show.show_price=sprice
                this_show.show_stime=sstime
                this_show.show_etime=setime
                db.session.commit()
                admin_login_status='show_updated'
                return render_template('adminpage.html', admin_login_status=admin_login_status)
            except:
                db.session.rollback()
                admin_login_status='no_show_update'
                return render_template('adminpage.html', admin_login_status=admin_login_status)
            finally:
                db.session.close()
        elif request.form['operation']=='update_venue':
            vname=request.form['vname']
            v_id=int(request.form['v_id'])
            vplace=request.form['vplace']
            vlocation=request.form['vlocation']
            vcapacity=request.form['vcapacity']
            if len(vname)>0 and len(vplace)>0 and len(vlocation)>0 and len(vcapacity)>0:
                if vplace.isalpha() and vlocation.isalpha() and vcapacity.isdigit():
                    venue = Venue.query.filter_by(venue_id=v_id).first()
                    try:
                        venue.venue_name=vname
                        venue.venue_place=vplace
                        venue.venue_location=vlocation
                        venue.venue_capacity=vcapacity
                        seat=Seats.query.filter_by(venue_id=v_id).all()
                        for each_seat in seat:
                            each_seat.no_seats=vcapacity
                        db.session.commit()
                        admin_login_status='venue_updated'
                        return render_template('adminpage.html', admin_login_status=admin_login_status)
                    except:
                        db.session.rollback()
                        admin_login_status='no_venue_update'
                        return render_template('adminpage.html', admin_login_status=admin_login_status)
                    finally:
                        db.session.close()
            else:
                admin_login_status='not_filled_venue'
                return render_template('adminpage.html', admin_login_status=admin_login_status, v_id=v_id)            
        elif request.form['operation']=='search':
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
            return render_template('admin.html', venues=venues, emp_id=email)    
    if request.method=='GET':
        emp_id=current_user.email
        i=emp_id.index("@")
        emp_id=emp_id[:i]
        venues = Venue.query.all()
        return render_template('admin.html', emp_id=emp_id, venues=venues)
# Home dashboard
@app.route('/admin/home', methods=['POST', 'GET'])
@login_required
@roles_required('admin')
def admin_home():
    empid = current_user.id
    tickets=Ticket.query.all()
    shows=Show.query.with_entities(Show.show_id, Show.show_name).all()
    venue=Show.query.with_entities(Venue.venue_id).all()
    sh_dic={}
    for tup in shows:
        if tup not in sh_dic:
            sh_dic[tup]={}
    for sh in sh_dic:
        for tup in venue:
            if tup[0] not in sh_dic[sh]:
                sh_dic[sh][tup[0]]=0
    for ticket in tickets:
        for key1 in sh_dic:
            if int(ticket.show_id)==int(key1[0]):
                for vid in sh_dic[key1]:
                    if int(vid)==int(ticket.venue_id):
                        sh_dic[key1][vid]+=ticket.no_seats
    shows=[]
    for show in sh_dic:
        if show[1] not in shows:
            data=[]
            for venue in sh_dic[show]:
                data.append(sh_dic[show][venue])
            plt.hist(data)
            plt.xlabel("Venues")
            plt.ylabel("No of tickets booked")
            mypath = os.path.abspath('static/img')
            myfile=show[1]+".png"
            plt.savefig(os.path.join(mypath, myfile))
            shows.append(show[1])
    return render_template('home.html',empid=empid, shows=shows)

# Create venue
@app.route('/admin/create_venue', methods=['POST', 'GET'])
@login_required
@roles_required('admin')
def create_venue():
    empid=current_user.email
    i=empid.index("@")
    empid=empid[:i]
    return render_template('venue.html',emp_id=empid)

@app.route('/admin/update_venue/<int:v_id>', methods=['POST','GET'])
@login_required
@roles_required('admin')
def update_venue(v_id):
    empid=current_user.email
    i=empid.index("@")
    empid=empid[:i]
    venue = Venue.query.filter_by(venue_id=v_id).first()
    return render_template('vedit.html',emp_id=empid, venue=venue)

@app.route('/admin/delete_venue/<int:v_id>', methods=['POST','GET'])
@login_required
@roles_required('admin')
def delete_venue(v_id):
    empid=current_user.email
    i=empid.index("@")
    empid=empid[:i]
    venue = Venue.query.filter_by(venue_id=v_id).first()
    
    for show in venue.shows:
        seat=Seats.query.filter_by(venue_id=v_id, show_id=show.show_id).first()
        db.session.delete(seat)
        db.session.commit()
        venue_show=Venue_Shows.query.filter_by(venue_id=v_id, show_id=show.show_id).first()
        db.session.delete(venue_show)
        db.session.commit()
        db.session.delete(show)
        db.session.commit()
    db.session.delete(venue)
    db.session.commit()
    admin_login_status='deleted_venue'
    return render_template('adminpage.html',admin_login_status=admin_login_status)

@app.route('/ts/admin/delete/<int:v_id>', methods=['POST', 'GET'])
@login_required
@roles_required('admin')
def delete(v_id):
    admin_login_status='delete_confirmation'
    return render_template('adminpage.html',admin_login_status=admin_login_status, v_id=v_id)

# Create slots
@app.route('/admin/create_show>', methods=['POST','GET'])
@login_required
@roles_required('admin')
def create_show():
    venues=Venue.query.all()
    empid=current_user.email
    i=empid.index("@")
    empid=empid[:i]
    return render_template('show.html',emp_id=empid, venues=venues)

@app.route('/admin/theatre/<int:vid>', methods=['POST', 'GET'])
@login_required
def atheatre_view(vid):
    venues = Venue.query.filter_by(venue_id=vid).first()
    emp_id=current_user.email
    i=emp_id.index("@")
    emp_id=emp_id[:i]
    return render_template('avenueview.html', emp_id=emp_id, venues=venues)
@app.route('/admin/show/<int:s_id>/<int:v_id>', methods=['POST','GET'])
@login_required
@roles_required('admin')
def show_action(s_id, v_id):
    venue = Venue.query.filter_by(venue_id=v_id).first()
    seat = Seats.query.filter_by(venue_id=v_id, show_id=s_id).first()
    this_show=None
    for show in venue.shows:
        if show.show_id==s_id:
            this_show=show
            break   
    sstime=show.show_stime.strftime("%H:%M")
    setime=show.show_etime.strftime("%H:%M")
    empid=current_user.email
    i=empid.index("@")
    empid=empid[:i]
    return render_template('action.html',emp_id=empid, show=this_show, venue=venue, seat=seat)
# ******* User's routers end here *******
