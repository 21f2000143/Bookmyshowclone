from flask import render_template, request, redirect, url_for, session
from flask import current_app as app
import string
from .database import db
from .models import *
from datetime import datetime
import os
#applying sending mail feature

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# ******* Admin's routers start here *******
# admin login router
@app.route('/ts/admin/login', methods=['GET'])
def admin_login():
    return render_template('adminlogin.html')

# admin login validation   
@app.route('/ts/admin/validation', methods=['POST', 'GET'])
def admin_validation():
    if request.method=='POST':
        admin_login_status='success'
        empid = request.form['Email']
        if empid is not None:
            pasw = request.form['password']
            if pasw is not None:
                if "@" not in empid:
                    admin_login_status='invalid_email'
                    return render_template('adminpage.html', admin_login_status=admin_login_status)            
                admin = Admin.query.first()
                if admin is not None:
                    if admin.emp_id==empid:
                        if admin.emp_pass==pasw:
                            session['adminname']=empid
                            app.logger.info("Admin login successfully!")
                            return render_template('adminpage.html', admin_login_status=admin_login_status, empid=empid)
                        else:
                            admin_login_status='incorrect_password'
                            return render_template('adminpage.html', admin_login_status=admin_login_status)
                    else:
                        admin_login_status='no_admin_found'
                        return render_template('adminpage.html', admin_login_status=admin_login_status)
                else:
                    admin_login_status='no_admin_found'
                    return render_template('adminpage.html', admin_login_status=admin_login_status)
            else:
                admin_login_status='empty'
                return render_template('adminpage.html', admin_login_status=admin_login_status)
        else:
            admin_login_status='empty'
            return render_template('adminpage.html', admin_login_status=admin_login_status)
    if request.method=='GET':
        if 'adminname' in session:
            admin_login_status='success'
            return render_template('adminpage.html', admin_login_status=admin_login_status, empid=session['adminname'])            
        return redirect(url_for('admin_login'))
# Admin dashboard
@app.route('/ts/admin/dashboard', methods=['POST','GET'])
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
                        admin = Admin.query.first()
                        emp_id=admin.emp_id
                        i=emp_id.index("@")
                        emp_id=emp_id[:i]
                        venues = Venue.query.all()
                        return render_template('admin.html', emp_id=emp_id, venues=venues)
                else:
                    admin_login_status='invalid_data_literal_venue'
                    return render_template('adminpage.html', admin_login_status=admin_login_status)
            else:
                admin_login_status='not_filled'
                return render_template('adminpage.html', admin_login_status=admin_login_status)
        elif request.form['operation']=='create_show':
            sname=request.form['sname']
            stag=request.form['stag']
            sprice=request.form['sprice']
            # sseats=request.form['sseats']
            sstime=request.form['sstime']
            setime=request.form['setime']
            v_id=int(request.form['v_id'])
            if len(sname)>0 and len(stag)>0 and len(sprice)>0 and len(setime)>0 and len(sstime)>0:
                if stag.isalpha() and sprice.isdigit() and (setime>sstime):
                    venue=Venue.query.filter_by(venue_id=v_id).first()
                    if sname in [show.show_name for show in venue.shows]:
                        admin_login_status='show_already_exist'
                        return render_template('adminpage.html', admin_login_status=admin_login_status,v_id=v_id)
                    else:
                        date_format="%H:%M"
                        sstime=datetime.strptime(sstime, date_format)
                        setime=datetime.strptime(setime, date_format)
                        show=Show(show_name=sname, show_tag=stag, show_price=sprice, no_seats=int(venue.venue_capacity), show_stime=sstime, show_etime=setime)
                        db.session.add(show)
                        venue.shows.append(show)
                        db.session.commit()

                        admin = Admin.query.first()
                        emp_id=admin.emp_id
                        i=emp_id.index("@")
                        emp_id=emp_id[:i]
                        venues = Venue.query.all()
                        return render_template('admin.html', emp_id=emp_id, venues=venues)
                else:
                    admin_login_status='invalid_data_literal_show'
                    return render_template('adminpage.html', admin_login_status=admin_login_status,v_id=v_id)
            else:
                admin_login_status='not_filled'
                return render_template('adminpage.html', admin_login_status=admin_login_status, v_id=v_id)
        elif request.form['operation']=='show_delete' :
            v_id=int(request.form['v_id'])
            s_id=int(request.form['s_id'])
            venue = Venue.query.filter_by(venue_id=v_id).first()
            for show in venue.shows:
                if show.show_id==s_id:
                    venue.shows.remove(show)
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
            # sseats=request.form['sseats']
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
    if request.method=='GET':
        if 'adminname' in session:
            admin = Admin.query.first()
            emp_id=admin.emp_id
            i=emp_id.index("@")
            emp_id=emp_id[:i]
            venues = Venue.query.all()
            return render_template('admin.html', emp_id=emp_id, venues=venues)
        else:
            return redirect(url_for('admin_login'))
# Home dashboard
@app.route('/ts/admin/home', methods=['POST', 'GET'])
def admin_home():
    if 'adminname' in session:
        admin = Admin.query.first()
        empid = admin.emp_id
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
    else:
        return redirect(url_for('admin_login'))

# Create venue
@app.route('/ts/admin/create_venue', methods=['POST', 'GET'])
def create_venue():
    if 'adminname' in session:
        admin = Admin.query.first()
        empid=admin.emp_id
        i=empid.index("@")
        empid=empid[:i]
        return render_template('venue.html',emp_id=empid)
    else:
        return redirect(url_for('admin_login'))

@app.route('/ts/admin/update_venue/<int:v_id>', methods=['POST','GET'])
def update_venue(v_id):
    if 'adminname' in session:
        admin = Admin.query.first()
        empid=admin.emp_id
        i=empid.index("@")
        empid=empid[:i]
        venue = Venue.query.filter_by(venue_id=v_id).first()
        return render_template('vedit.html',emp_id=empid, venue=venue)
    else:
        return redirect(url_for('admin_login'))

@app.route('/ts/admin/delete_venue/<int:v_id>', methods=['POST','GET'])
def delete_venue(v_id):
    if 'adminname' in session:
        admin = Admin.query.first()
        empid=admin.emp_id
        i=empid.index("@")
        empid=empid[:i]
        venue = Venue.query.filter_by(venue_id=v_id).first()
        for show in venue.shows:
            db.session.delete(show)
            db.session.commit()
        db.session.delete(venue)
        db.session.commit()
        admin_login_status='deleted_venue'
        return render_template('adminpage.html',admin_login_status=admin_login_status)
    else:
        return redirect(url_for('admin_login'))
@app.route('/ts/admin/delete/<int:v_id>', methods=['POST', 'GET'])
def delete(v_id):
    if 'adminname' in session:
        admin_login_status='delete_confirmation'
        return render_template('adminpage.html',admin_login_status=admin_login_status, v_id=v_id)
    else:
        return redirect(url_for('admin_login'))

# Create slots
@app.route('/ts/admin/create_show/<int:v_id>', methods=['POST','GET'])
def create_show(v_id):
    if 'adminname' in session:
        admin = Admin.query.first()
        venue=Venue.query.filter_by(venue_id=v_id).first()
        empid=admin.emp_id
        i=empid.index("@")
        empid=empid[:i]
        return render_template('show.html',emp_id=empid, venue=venue)
    else:
        return redirect(url_for('admin_login'))

@app.route('/ts/admin/show/<int:s_id>/<int:v_id>', methods=['POST','GET'])
def show_action(s_id, v_id):
    if 'adminname' in session:
        venue = Venue.query.filter_by(venue_id=v_id).first()
        this_show=None
        for show in venue.shows:
            if show.show_id==s_id:
                this_show=show
                break   
        sstime=show.show_stime.strftime("%H:%M")
        setime=show.show_etime.strftime("%H:%M")
        admin = Admin.query.first()
        empid=admin.emp_id
        i=empid.index("@")
        empid=empid[:i]
        return render_template('action.html',emp_id=empid, show=this_show, venue=venue)
    else:
        return redirect(url_for('admin_login'))
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    if 'adminname' in session:
        session.pop('adminname')
    return redirect(url_for('admin_login'))
# ******* Admin's routers end here *******
