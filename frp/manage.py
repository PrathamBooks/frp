#!/usr/bin/env python

import datetime
import os
import subprocess

from flask.ext.script import Manager
from frp.startup.init_app import init_app

from frp import app
from frp.models import db
from frp.models import (User, UserInfo, UserAuth, USER_STATUS, is_email_exists,
                        Organization, OrganizationInfo, OrganizationWork, Campaign, Donation)
from flask import current_app

manager = Manager(app)
init_app(app)
db.init_app(app)
db.app = app

@manager.command
def runserver():
    """
    Runs the flask development server using the specified config file.

    Defaults to settings/development.py
    """
    global settings
    db.create_all()
    app.run()

@manager.command
def resetdb():
    global settings, db
    print "Dropping all tables"
    db.drop_all()
    print "Creating them afresh"
    db.create_all()

@manager.command
def seed():
    import datetime
    user = User(status=USER_STATUS.ACTIVE, email='kuchlous@gmail.com',
            first_name='Alok', last_name='Kuchlous', active=True,
            confirmed_at=datetime.datetime.now())
    db.session.add(user)

    user_auth = UserAuth(password=current_app.user_manager.hash_password('kuchlous'), 
            user=user, active=True)
    db.session.add(user_auth)

    user_info = UserInfo(
        user=user,  address='502, TZed Homes',
        contact_number='990232323232',
        pan_number='XXYYZZ')
    db.session.add(user_info)

    org = Organization(title='Whitefield Awake', created_by=user)
    db.session.add(org)

    # Create org info
    org_info = OrganizationInfo(
         org=org, email='info@example.com', category=2, status=1, address='123, Street 2',
         contact_number='99010201011', facebook='http://facebook.com/mirafra', 
         website='http://www.mirafra.com',
         has_80g_certificate='t', person1_name='Alok',
         person1_position='CEO', person1_email='kuchlous@gmail.com',
         person2_position='COO', person2_email='shyam@example.com',
         person1_phone='898923232328', person2_name='shyam',
         person2_phone='89323232899', 
         total_impact_on_children='2000')
    db.session.add(org_info)

    work = OrganizationWork(organization=org, choice_id='3') 

    campaign = Campaign(created_by=user, org=org,
            title='Buy a 1000 books', description='Project to get 1000 books for Ramagondanhalli School', 
            who='We are an organization of volunteers', impact='This will raise funds to buy 1000 books for government schools',
            utilization='A very large impact', state="Haryana", city="Karnal", nbooks='1000', nlic=0, languages="Hindi, Tamil",
            image="1.jpg", status="Submitted")
    db.session.add(campaign)

    campaign = Campaign(created_by=user, org=org,
            title='Rural Library', description='Project to set up a rural library', 
            who='We are an organization who works in rural AP', impact='This will raise funds to set up a new library.',
            utilization='Utilize to get books', state="Andhra Pradesh", city="Hyderabad", nbooks='500', nlic=2, languages="Telugu, English",
            image="2.jpg", status="Approved")
    db.session.add(campaign)

    campaign = Campaign(created_by=user, org=org,
            title='Urban Library', description='Project to get 750 books for old age home', 
            who='We are an organization of old people', impact='Make 100 old people happy',
            utilization='It will help a few old people smile', state="Karnataka", city="Dharwad", nbooks='100', nlic=0, languages="English, Tamil",
            image="3.jpg", status="Shipped")
    db.session.add(campaign)

    campaign = Campaign(created_by=user, org=org,
            title='Slum Library', description='Slum library in Dharavi, Mumbai', 
            who='We are an organization of volunteers', impact='Library for street children',
            utilization='Take children off the streets', state="Maharashtra", city="Mumbai", nbooks='10000', nlic=0, languages="Hindi, Punjabi",
            image="4.jpg", status="Ended")
    db.session.add(campaign)

    donation = Donation(donor=user, campaign=campaign, amount=10000, confirmation=53499)
    db.session.add(donation)

    campaign = Campaign(created_by=user, org=org,
            title='Buy a 1000 books', description='Project to get 1000 books for Sidhapura School', 
            who='We are an organization of volunteers', impact='This will raise funds to buy 1000 books for government schools',
            utilization='A very large impact', state="Karnataka", city="Bangalore", nbooks='1000', nlic=0, languages="Kannada, Tamil",
            image="5.jpg", status="Delivered")
    db.session.add(campaign)

    donation = Donation(donor=user, campaign=campaign, amount=5000, confirmation=93499)
    db.session.add(donation)

    campaign = Campaign(created_by=user, org=org,
            title='Buy a 1000 books', description='Project to get 1000 books for Ramagondanhalli School', 
            who='We are an organization of volunteers', impact='This will raise funds to buy 1000 books for government schools',
            utilization='A very large impact', state="Haryana", city="Karnal", nbooks='1000', nlic=0, languages="Hindi, Tamil",
            image="6.jpg", status="Flagged")
    db.session.add(campaign)

    donation = Donation(donor=user, campaign=campaign, amount=1000, confirmation=99999)
    db.session.add(donation)

    try:
        db.session.commit()
        print 'Successfully seeded'
    except Exception as e:
        print e
        app.logger.warning('Unable to save')
        db.session.rollback()
 
 
if __name__ == '__main__':
    manager.run()
