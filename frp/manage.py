#!/usr/bin/env python

import datetime
import os
import subprocess

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from frp import app
from frp.models import db
from frp.models import (User, UserInfo, USER_STATUS, is_email_exists,
                      Organization, OrganizationInfo, OrganizationWork, Campaign)

manager = Manager(app)
db.init_app(app)
db.app = app

settings = "settings/development.py"
test_settings = "settings/testing.py"
settings = os.environ.get('APP_SETTINGS', settings)
print "Loading config from %s" % settings


migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def runserver():
    """
    Runs the flask development server using the specified config file.

    Defaults to settings/development.py
    """
    global settings
    app.config.from_pyfile(settings)
    db.create_all()
    app.run()


# @manager.command
# def migrate():
#     """
#     Runs alembic migration
#     """
#     global settings
#     app.config.from_pyfile(settings)
#     db.create_all()
#     ManageMigrations().run()


@manager.command
def resetdb():
    global settings, db
    app.config.from_pyfile(settings)
    print "Dropping all tables"
    db.drop_all()
    print "Creating them afresh"
    db.create_all()
    print "Creating lastuser tables"

@manager.command
def seed():
    user = User(status=USER_STATUS.INVITED, email='kuchlous@gmail.com',
            password='kuchlous', _username='kuchlous')
    db.session.add(user)

    user_info = UserInfo(
        user=user, first_name='Alok',
        last_name='Kuchlous', address='502, TZed Homes',
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
            image="1.jpg")
    db.session.add(campaign)

    campaign = Campaign(created_by=user, org=org,
            title='Rural Library', description='Project to set up a rural library', 
            who='We are an organization who works in rural AP', impact='This will raise funds to set up a new library.',
            utilization='Utilize to get books', state="Andhra Pradesh", city="Hyderabad", nbooks='500', nlic=2, languages="Telugu, English",
            image="2.jpg")
    db.session.add(campaign)

    campaign = Campaign(created_by=user, org=org,
            title='Urban Library', description='Project to get 750 books for old age home', 
            who='We are an organization of old people', impact='Make 100 old people happy',
            utilization='It will help a few old people smile', state="Karnataka", city="Dharwad", nbooks='100', nlic=0, languages="English, Tamil",
            image="3.jpg")
    db.session.add(campaign)

    campaign = Campaign(created_by=user, org=org,
            title='Slum Library', description='Slum library in Dharavi, Mumbai', 
            who='We are an organization of volunteers', impact='Library for street children',
            utilization='Take children off the streets', state="Maharashtra", city="Mumbai", nbooks='10000', nlic=0, languages="Hindi, Punjabi",
            image="4.jpg")
    db.session.add(campaign)

    campaign = Campaign(created_by=user, org=org,
            title='Buy a 1000 books', description='Project to get 1000 books for Sidhapura School', 
            who='We are an organization of volunteers', impact='This will raise funds to buy 1000 books for government schools',
            utilization='A very large impact', state="Karnataka", city="Bangalore", nbooks='1000', nlic=0, languages="Kannada, Tamil",
            image="5.jpg")
    db.session.add(campaign)

    campaign = Campaign(created_by=user, org=org,
            title='Buy a 1000 books', description='Project to get 1000 books for Ramagondanhalli School', 
            who='We are an organization of volunteers', impact='This will raise funds to buy 1000 books for government schools',
            utilization='A very large impact', state="Haryana", city="Karnal", nbooks='1000', nlic=0, languages="Hindi, Tamil",
            image="6.jpg")
    db.session.add(campaign)
    try:
        db.session.commit()
        print 'Successfully seeded'
    except Exception as e:
        print e
        app.logger.warning('Unable to save')
        db.session.rollback()
 
 
if __name__ == '__main__':
    manager.run()
