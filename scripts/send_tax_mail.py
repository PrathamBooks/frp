#!/usr/bin/env python

import sys
sys.path.append("/home/infodigital/frp/frp")

from flask.ext.script import Manager

from datetime import *
from frp import app
from frp.models import db
from frp.models import Donation, Receipt
from frp.models import User

import smtplib
from num2words import num2words

import base64

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, render_template, redirect, url_for
from flask.ext.mail import Mail, Message
from subprocess import call
from flask.ext.mandrill import Mandrill

manager = Manager(app)
mail_ext = Mail(app)

app.config['MANDRILL_API_KEY'] = 'rgN2mMD61Fma_qLk7Uf6jw'
app.config['MANDRILL_DEFAULT_FROM'] = 'donateabook@prathambooks.org'
mandrill = Mandrill(app)

RECEIPTS_DIR = "/home/infodigital/tax-receipts/"

# From http://flask.pocoo.org/snippets/68/
def create_pdf(pdf_data, pdf_file_name):
    html_file_name = "tax_mail.html"
    temphtmlfile = open(html_file_name, "w")
    temphtmlfile.write(pdf_data)
    temphtmlfile.close()
    call("/usr/local/bin/wkhtmltopdf " + html_file_name + " " + RECEIPTS_DIR+pdf_file_name, shell=True)

def get_financial_year(donation):
    if (donation.created_at.month > 3):
        return donation.created_at.year
    else:
        return donation.created_at.year - 1

def get_serial_number(donation):
    year = get_financial_year(donation)
    start_date = datetime(year, 4, 1)
    end_date = datetime(year + 1, 3, 31)
    last_receipt = Receipt.query.join(Donation).filter(Donation.created_at >= start_date).filter(Donation.created_at <= end_date).order_by(Receipt.serial_num.desc()).first()
    if (last_receipt):
        last_serial_number = last_receipt.serial_num
    else:
        last_serial_number = 0
    return last_serial_number + 1

def get_pdf_file_name(receipt):
    serial_num = receipt.serial_num 
    year = get_financial_year(receipt.donation)
    pdf_file_name = "dab_eReceipt_PB" + str(serial_num) + "_" + str(year) + "_" + str(year + 1) + ".pdf"
    return pdf_file_name

def create_receipt_for_donation(donation):
    receipt = None
    receipts = donation.receipt
    if (len(receipts) > 0):
      receipt = receipts[0]
     
    if (not receipt):
        print "Creating Receipt"
        serial_number = get_serial_number(donation)
        serial_string = "PB" + \
               str(serial_number).zfill(4) + \
               "/" + \
               str(get_financial_year(donation)) + \
               "-" + \
               str(get_financial_year(donation) + 1)[2:4]

        receipt = Receipt(donation=donation,
                serial_num=serial_number,
                serial_string=serial_string,
                mail_date=datetime.now())
        db.session.add(receipt)
        db.session.commit()
    return receipt

def send_mails_for(useremail):
    donor = User.query.filter(User.email == useremail).one()
    donations = donor.donations
    for donation in donations:
	if donation.confirmation != None:
            print str(donation.id) + ' ' + donation.donor.email + ' ' + donation.identification + ' ' + donation.confirmation + ' ' + str(donation.tax_exemption_certificate) + ' ' + "{:%B %d, %Y}".format(donation.created_at)
            receipt = create_receipt_for_donation(donation)
            send_mail_for_donation(donation, receipt)


def send_mails_after(days):
    now = datetime.now()
    past_0 = now - timedelta(days=days)
    past_1 = now - timedelta(days=days+1)
    donations = Donation.query.filter(Donation.created_at <= past_0,
                                      Donation.created_at > past_1,
                                      Donation.confirmation != '',
                                      Donation.tax_exemption_certificate == True,
                                      Donation.confirmation != None).all()
    for donation in donations:
	if donation.confirmation != None:
            print str(donation.id) + ' ' + donation.donor.email + ' ' + donation.identification + ' ' + donation.confirmation + ' ' + str(donation.tax_exemption_certificate) + ' ' + "{:%B %d, %Y}".format(donation.created_at)
            receipt = create_receipt_for_donation(donation)
            send_mail_for_donation(donation, receipt)

def send_old_mails():
    past_1 = datetime(2015, 9, 24)
    past_0 = datetime(2015, 11, 11)
    donations = Donation.query.filter(Donation.created_at <= past_0,
                                      Donation.created_at > past_1,
                                      Donation.confirmation != '',
                                      Donation.tax_exemption_certificate == True,
                                      Donation.confirmation != None).all()
    for donation in donations:
        print str(donation.id) + ' ' + donation.donor.email + ' ' + donation.identification + ' ' + donation.confirmation + ' ' + str(donation.tax_exemption_certificate) + ' ' + "{:%B %d, %Y}".format(donation.created_at)
        receipt = create_receipt_for_donation(donation)
        send_mail_for_donation(donation, receipt)

def create_pdf_for_donation(donation, receipt):
    html = render_template('tax_mail.html', donation=donation, amount_string=num2words(donation.amount).capitalize(), receipt=receipt)
    pdf_file_name = get_pdf_file_name(receipt)
    create_pdf(html, pdf_file_name)
    return pdf_file_name

def send_mail_for_donation(donation, receipt):
    pdf_file_name = create_pdf_for_donation(donation, receipt)
    with open(RECEIPTS_DIR+pdf_file_name, 'rb') as fp:
       pdf = base64.b64encode(fp.read())

    # https://github.com/volker48/flask-mandrill
    mandrill.send_email(
     	from_email='donateabook@prathambooks.org',
      	subject='eReceipt of your donation on Donate-a-Book',
      	to=[{'email': donation.donor.email}, {'email': 'ereceipts@prathambooks.org', 'type': 'cc'}],
      	text="Dear " + donation.donor.profile_name() + ",\n\n" + "We wish to express our heartfelt gratitude for your contribution of Rs. " + str(donation.amount) + ". on " + "{:%d/%m/%Y}".format(donation.created_at) + " towards Pratham Books' Donate-a-Book platform. Your support has been significant in helping India's children read. \n\nYour donation is tax deductible in India. We've attached a PDF copy of your eReceipt with this email. For any further information on your donation, please contact donateabook@prathambooks.org.\n\nThanking You.\n\nRegards,\n\nTeam Donate-a-Book",
        attachments=[{'type': 'application/pdf', 'name': pdf_file_name, 'content': pdf}]
    )

@manager.command
def mail():
    send_mails_after(30)
    # send_mails_for("senthilcool@gmail.com")
    # send_mails_for("kuchlous@gmail.com")

if __name__ == '__main__':
     manager.run()
