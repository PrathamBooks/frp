#!/usr/bin/env python

import sys
sys.path.append("/home/infodigital/frp/frp")

from flask.ext.script import Manager

from datetime import *
from frp import app
from frp.models import db
from frp.models import Campaign

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


manager = Manager(app)

def send_email(to, subject, text):
    if not isinstance(to, list):
        to = [to]
    sender = 'noreply@donateabook.org'
    msg = MIMEMultipart()
    msg['Subject'] = subject
    i=MIMEText(text, 'plain')
    msg.attach(i)

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, to, msg.as_string())
        print "Successfully sent email"
    except SMTPException:
        print "Error: unable to send email"

def close_campaigns():
    campaigns_last_day_today = Campaign.last_day_today()
    for campaign in campaigns_last_day_today:
        campaign.status = 'Closed'
        db.session.add(campaign)
        try:
          db.session.commit()
        except Exception as e:
          print e,"Unable to Commit"

        name = campaign.created_by.profile_name()
        campaign_title = campaign.title
        percent = campaign.percent_funded()

        text = 'Dear ' + name + ',\n\nWhat a ride that was! Your Donate-a-Book Campaign: ' + campaign_title + ' has officially come to an end.\n'+ 'You have raised ' + str(percent) + ' of your target fund. Congratulations on the success of your campaign. \n\nYou can expect to receive an email from the Pratham Books team which will have a comprehensive list of all books in stock. You would be able to pick and choose your preferred books priced within the fund limit that you have raised.\nKeep an eye out for our email, we will be in touch soon with more details. \n\nRegards, \nDonate-a-Book Team'
        send_email(to=campaign.emails(),
                subject="Congratulations on the success of your campaign!",
                text=text)
 
def send_last_week_mails():
    campaigns_last_week = Campaign.last_week()
    for campaign in campaigns_last_week:
        name = campaign.created_by.profile_name()
        campaign_title = campaign.title
        end_date = "{:%B %d, %Y}".format(campaign.end_date())

        text = 'Dear ' + name + ',\n\nYour campaign with title: ' + campaign_title + ' ends on ' + end_date +'. You are just 7 days away from completion.\nPull up your socks, give it a final push and meet your targets. Our books await you.\nGood Luck. Let it be your best foot forward. \n\nRegards,\nDonate-a-Book Team'
        send_email(to=campaign.emails(),
                subject="Just 7 days to go!",
                text=text
                )

@manager.command
def mail():
    print "Entered campaign_close_and_mail"
    close_campaigns()
    send_last_week_mails()

if __name__ == '__main__':
     manager.run()
