#!/usr/bin/env python

#import datetime
import os
import subprocess

from flask.ext.script import Manager

from datetime import *
from frp import app
from frp.models import db
from frp.models import (User, UserAuth, Role, USER_STATUS, is_email_exists,
                        Organization, OrganizationInfo, OrganizationWork, Campaign, Donation,Comment)
from flask import current_app
from apscheduler.schedulers.blocking import BlockingScheduler
from frp.mailer import Mailer
import logging
from logging import FileHandler

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


manager = Manager(app)
scheduler = BlockingScheduler()
file_handler = FileHandler('server.log')
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)




def send_email(to,name,title,percent,subject,start_date):
    if not isinstance(to, list):
        to = [to]
    sender = 'noreply@donateabook.org'
    receivers = ['sairamsudhir@mirafra.com']
    msg = MIMEMultipart()
    msg['Subject'] = subject
    text = 'Dear '+name+'\n\nWhat a ride that was! Your Donate-a-Book Campaign: '+title+' has officially come to an end.\n'+ 'You have raised ' + str(percent) + ' of  your target fund. Congratulations on the success of your campaign. \n\nYou can expect to receive an email from the Pratham Books team which will have a comprehensive list of all books in stock.You would be able to pick and choose your preferred books priced within the fund limit that you have raised.\nKeep an eye out for our email, we will be in touch soon with more details \n\nRegards, \nDonate-a-Book Team'

    i=MIMEText(text, 'plain')
    msg.attach(i)

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, to, msg.as_string())
        print "Successfully sent email"
    except SMTPException:
        print "Error: unable to send email"

def send_mail():
    campaigns = Campaign.all_campaigns_data(is_last_day=True)
    for campaign in campaigns:
        campaign.status = 'Closed'
        db.session.add(campaign)
        try:
          db.session.commit()
        except Exception as e:
          print e,"Unable to Commit"

        send_email(to=campaign.created_by.email,
                subject="Congratulations on the success of your campaign!",
                name=campaign.created_by.first_name,
                title=campaign.title,
                percent=campaign.percent_funded(),
                start_date="{:%B %d, %Y}".format(campaign.start_date()))


@manager.command
def cron():
    scheduler.add_job(send_mail, 'interval', days=1)
    scheduler.start()

@manager.command
def mail():
    send_mail()

if __name__ == '__main__':
     manager.run()
