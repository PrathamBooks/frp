#!/usr/bin/env python

import sys
sys.path.append("/home/infodigital/frp/frp")

from flask.ext.script import Manager

from datetime import *
from frp import app
from frp.models import db
from frp.models import Donation
from frp.models import User

import smtplib
from num2words import num2words

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, render_template, redirect, url_for
from flask.ext.mail import Mail, Message
from subprocess import call

manager = Manager(app)
mail_ext = Mail(app)

# From http://flask.pocoo.org/snippets/68/
def create_pdf(pdf_data):
    html_file_name = "tax_mail.html"
    temphtmlfile = open(html_file_name, "w")
    temphtmlfile.write(pdf_data)
    temphtmlfile.close()
    pdf_file_name = "tax_mail.pdf"
    call("/usr/local/bin/wkhtmltopdf " + html_file_name + " " + pdf_file_name, shell=True)
    return pdf_file_name

def get_financial_year(donation):
    if (donation.created_at.month > 3):
        return donation.created_at.year
    else:
        return donation.created_at.year - 1

def get_serial_number(donation):
    year = get_financial_year(donation)
    start_date = datetime.datetime(year, 4, 1)
    end_date = datetime.datetime(year + 1, 3, 31)
    last_receipt = Receipt.query.join(Donation).filter(Donation.created_at >= start_date).filter(Donation.created_at <= end_date).order_by(Receipt.serial_number.desc()).first()
    if (last_receipt):
        last_serial_number = last_receipt.serial_number
    else:
        last_serial_number = 0
    return last_serial_number + 1

def create_receipt_for_donation(donation):
    receipt = donation.receipt
    if (not receipt):
        print "Creating Receipt"
        serial_number = get_serial_number(donation)
        serial_string = "PB" + \
               str(serial_number).zfill(4) + \
               "/" + \
               str(get_financial_year(donation)) + \
               "-" + \
               str(get_financial_year(donation))[2:4]

        receipt = Receipt(donation=donation,
                serial_number=serial_number,
                serial_string=serial_string,
                mail_date=datetime.datetime.now())
        db.session.add(receipt)
        db.session.commit()
    return receipt

def send_mails_after(days):
    now = datetime.now()
    past_0 = now - timedelta(days=days)
    past_1 = now - timedelta(days=days+1)
    donations = Donation.query.filter(Donation.created_at <= past_0,
                                      Donation.created_at > past_1,
                                      Donation.confirmation != '',
                                      Donation.tax_exemption_certificate == True).all()
    user = User.query.filter(User.email=="payoshni@prathambooks.org").first()
    donations = user.donations
    for donation in donations:
        receipt = create_receipt_for_donation(donation)
        send_mail_for_donation(donation, receipt)
        return

def create_pdf_for_donation(donation):
    html = render_template('tax_mail.html', donation=donation, amount_string=num2words(donation.amount).capitalize(), receipt=receipt)
    print html
    # pdf_file_name = create_pdf(html)
    # return pdf_file_name

def send_mail_for_donation(donation, receipt):
    pdf_file_name = create_pdf_for_donation(donation, receipt)
    to = [donation.donor.email, "kuchlous@gmail.com"]
    subject = "eReceipt of your donation on Donate-a-Book"
    mail_to_be_sent = Message(subject=subject, recipients=to, sender='noreply@donateabook.org')
    mail_to_be_sent.body = "Dear " + donation.donor.profile_name() + ",\n\n" + "We wish to express our heartfelt gratitude for your contribution of Rs. " + str(donation.amount) + ". on " + "{:%d/%m/%Y}".format(donation.created_at) + " towards Pratham Books' Donate-a-Book platform. Your support has been significant in helping India's children read. \n\nYour donation is tax deductible in India. We've attached a PDF copy of your eReceipt with this email. For any further information on your donation, please contact donateabook@prathambooks.org.\n\nThanking You.\n\nRegards,\n\nTeam Donate-a-Book"
    # with open(pdf_file_name, 'r') as fp:
    #   mail_to_be_sent.attach("tax_receipt.pdf", "application/pdf", fp.read())
    # mail_ext.send(mail_to_be_sent)

@manager.command
def mail():
    send_mails_after(30)

if __name__ == '__main__':
     manager.run()
