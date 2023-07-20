from application.workers import celery
from datetime import datetime
import time
# from main import gmail_service ---------there is problem with controllers, need to fix this--------
from flask_sse import sse
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from send import *
from .models import *
from flask import render_template
# import base64
from celery.schedules import crontab
# from celery.decorators import periodic_task

def mail_report():
    datadict=list()
    users=User.query.all()
    for user in users:
        if "user" in list(user.roles):
            temp=dict()
            temp['email']=user.email
            temp['tickets']=[]
            for tiket in user.tickets:
                show=Show.query.filter_by(show_id=tiket.show_id).first()
                if show:
                    temp2=dict()
                    temp2['show_name']=show.show_name
                    temp2['show_rating']=show.show_rating
                    temp2['show_tag']=show.show_tag
                    temp2['show_price']=show.show_price
                    temp2['show_stime']=show.show_stime
                    temp2['show_etime']=show.show_etime
                    temp2['no_seats']=tiket.no_seats
                    temp2['book_time']=tiket.book_time
                    temp['tickets'].append(temp2)
            datadict.append(temp)
    return render_template('mail_format.html', datadict=datadict)
# print("crontab ", crontab)

# def create_message(email, subject, message):
#     msg = MIMEText(message)
#     msg['to'] = email
#     msg['subject'] = subject
#     return {'raw': base64.urlsafe_b64encode(msg.as_string().encode()).decode()}


# def send_email(service, email, subject, message):
#     try:
#         message = create_message(email, subject, message)
#         service.users().messages().send(userId='me', body=message).execute()
#     except HttpError as error:
#         print(f"An error occurred: {error}")
# def create_message(email, subject, message):
#     message = {
#         'to': email,
#         'subject': subject,
#         'message': message
#     }
#     return message


# @celery.task
# def send_daily_reminder():
#     email = "21f2000143@ds.study.iitm.ac.in"
#     subject = "Daily Reminder"
#     message = "Don't forget your daily tasks!"
#     send_email(gmail_service, email, subject, message)
#     return "sent!"

# Schedule the daily reminder task
# from flask import current_app as app
# celery.conf.beat_schedule = {
#     'send-daily-reminder': {
#         'task': 'print_current_time_job',
#         'schedule': crontab(minute=1),  # Schedule at 8:00 AM every day
#     },
# }
celery.conf.timezone = 'Asia/Kolkata'

# @celery.task()
# def just_say_hello(name):
#     print("INSIDE TASK")
#     print("Hello {}".format(name))
#     return name



@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(crontab(hour=21, minute=0), daily_reminder_to_user.s(), name='at 10:30')
    sender.add_periodic_task(crontab(minute='*/2'), monthly_report_to_admin.s(), name='sending monthly report every 2 minutes')
    # sender.add_periodic_task(crontab(hour=6, minute=0, day_of_month=1, month_of_year='*/1'), monthly_report_to_admin.s(), name='at 10:30')


# @celery.task()
# def calculate_aggregate_likes(article_id):
#     # You can get all the likes for the `article_id`
#     # Calculate the aggregate and store in the DB
#     print("#####################################")
#     print("Received {}".format(article_id))
#     print("#####################################")
#     return True


# scheduled task
@celery.task()
def daily_reminder_to_user():
    print("Inside the task")
    now = datetime.now()
    print("now =", now)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # test send email
    send_message(service, "sachinthesensitive2@gmail.com", "This is a subject", 
            "This is the body of the email with alert", ["test.txt", "photo.jpg"])
    sse.publish({"message": "Current time ="+dt_string },type='greeting')
    print("date and time =", dt_string) 
    print("COMPLETE")
    return dt_string
# scheduled task
@celery.task()
def monthly_report_to_admin():
    print("Inside the task")
    now = datetime.now()
    print("now =", now)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # test send email
    body=mail_report()
    send_message(service, "sachinthesensitive2@gmail.com", "MONTHLY REPORT", 
            body, ["test.txt", "photo.jpg"])
    sse.publish({"message": "Current time ="+dt_string }, type='greeting')
    print("date and time =", dt_string) 
    print("COMPLETE")
    return dt_string

# user triggered task
@celery.task()
def user_triggerd_async_job():
    print("Inside the task")
    now = datetime.now()
    print("now =", now)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # test send email
    # send_message(service, "sachinthesensitive2@gmail.com", "This is a subject", 
    #         "This is the body of the email", ["test.txt", "photo.jpg"])
    sse.publish({"message": "Current time ="+dt_string }, type='greeting')
    print("date and time =", dt_string) 
    print("COMPLETE")
    return dt_string

# @celery.task()
# def long_running_job():
#     print("STARTED LONG JOB")
#     now = datetime.now()
#     dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#     sse.publish({"message": "STARTED ="+dt_string }, type='greeting')
#     for lp in range(100):
#         now = datetime.now()
#         print("now =", now)
#         dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#         sse.publish({"message": "RUNNING ="+dt_string }, type='greeting')
#         print("date and time =", dt_string) 
#         time.sleep(2)

#     now = datetime.now()
#     dt_string = now.strftime("%d/%m/%Y %H:%M:%S")        
#     sse.publish({"message": "COMPLETE ="+dt_string }, type='greeting')
#     print("COMPLETE LONG RUN")