#!/usr/bin/env python

import sys
sys.path.append("/home/infodigital/frp/frp")

from flask.ext.script import Manager

from datetime import *
from frp import app
from frp.models import db
from frp.models import Donation
from frp.models import User

from xhtml2pdf import pisa
from cStringIO import StringIO

import smtplib
from num2words import num2words

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, render_template, redirect, url_for
from flask.ext.mail import Mail, Message

manager = Manager(app)
mail_ext = Mail(app)

# From http://flask.pocoo.org/snippets/68/
def create_pdf(pdf_data):
    pdf = StringIO()
    pisa.CreatePDF(StringIO(pdf_data.encode('utf-8')), pdf)
    return pdf

def send_mails_after(days):
    now = datetime.now()
    past_0 = now - timedelta(days=days)
    past_1 = now - timedelta(days=days+1)
    donations = Donation.query.filter(Donation.created_at <= past_0,
                                      Donation.created_at > past_1,
                                      Donation.confirmation != '',
                                      Donation.tax_exemption_certificate == True).all()
    print len(donations)
    user = User.query.filter(User.email=="kuchlous@gmail.com").first()
    donations = user.donations
    for donation in donations:
        send_mail_for_donation(donation)
        return
    print user
    print len(donations)

def create_pdf_for_donation(donation):
    html = render_template('tax_mail.html', donation=donation, amount_string=num2words(donation.amount))
    print html
    pdf = create_pdf(html)
    return pdf

def send_mail_for_donation(donation):
    pdf = create_pdf_for_donation(donation)
    to = [donation.donor.email]
    subject = "Tax Certificate from Donate-A-Book"
    mail_to_be_sent = Message(subject=subject, recipients=to, sender='noreply@donateabook.org')
    mail_to_be_sent.body = "Dear " + donation.donor.profile_name() + ",\n" + "Here is the tax receipt you expected."
    mail_to_be_sent.attach("tax_receipt.pdf", "application/pdf", pdf.getvalue())
    mail_ext.send(mail_to_be_sent)

@manager.command
def mail():
    print "Entered send_tax_mail"
    send_mails_after(30)

if __name__ == '__main__':
     manager.run()
