from flask import render_template, redirect, url_for, request
from flask import current_app as app
from flask_security import current_user, login_required
from application.database import db_session
from .models import Venue, User, Role
from flask_security import roles_required


# User dashboard
@app.route('/', methods=['GET'])
def welcome():
    venues = Venue.query.all()
    return render_template('welcome.html', venues=venues)

@app.route('/redirecting', methods=['GET', 'POST'])
@login_required
def redirecting():
    if current_user.has_role('admin'):
        return redirect(url_for('admin_dashboard'))
    elif current_user.has_role('user'):
        return redirect(url_for('user_dashboard'))
    else:
        role = Role.query.filter_by(name='user').first()
        app.security.datastore.add_role_to_user(user=current_user, role=role)
        db_session.commit()
        return redirect(url_for('user_dashboard'))