from frp import app
from frp.models import db
from flask import current_app
from frp.models import (User, UserAuth, Role, USER_STATUS, is_email_exists,
                        Organization, OrganizationInfo, OrganizationWork, Campaign, 
                        Donation, Comment, Memory)
from flask_user import current_user, login_required, roles_required
import datetime
from BeautifulSoup import BeautifulSoup
import pytest
from conftest import add_user, add_org, add_campaign, add_donation, login, logout

# Initial Configuration

def test_add_user(test_db, seed_db, test_client):
    x = test_client.get("/")
    assert 'log in' in x.data
    x = login('user1@example.com','user1123',test_client)
    assert 'User 1' in x.data
    x = logout(test_client)
    assert 'log in' in x.data

def test_add_campaign(test_db, seed_db, test_client):
    # Check Data Base
    campaigns = Campaign.query.all()
    # Check Web
    for campaign in campaigns:
        x = test_client.get("/campaign/"+str(campaign.url()))
        assert campaign.title in x.data.decode('utf-8')

def test_add_donations(test_db, seed_db, test_client):
    with app.app_context():
        campaign = Campaign.query.all()[0]
        total_donations = campaign.total_donations()
        donation = add_donation(campaign, 1000)
        x = test_client.get("/campaign/"+str(donation.campaign.url()))
        soup = BeautifulSoup(x.data)
        total_donations += donation.amount
        percent_funded = (total_donations*100.0)/campaign.target()
        assert soup.find('div', {'class': "funds-raised"}).contents[1].text == str(int(round(percent_funded)))+'%'

def test_del_donations(test_db, seed_db, test_client):
    with app.app_context():
        campaign = Campaign.query.all()[0]
        for i in range(1,6):
            donation = add_donation(campaign, 1000)
        donation = Donation.query.filter_by(identification="ABCDEF").first()
        campaign = donation.campaign
        total_donations = campaign.total_donations()
        total_donations -= donation.amount
        db.session.delete(donation)
        db.session.commit()
        x = test_client.get("/campaign/"+str(campaign.url()))
        soup = BeautifulSoup(x.data)
        percent_funded = (total_donations*100.0)/campaign.target()
        assert soup.find('div', {'class': "funds-raised"}).contents[1].text == str(int(round(percent_funded)))+'%'

# Test that a closed campaign does not accept donations

# Test that a campaign which reaches its goal is automatically closed

# Test that an unapproved campaign does not accept donations
