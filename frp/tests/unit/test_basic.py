from frp import app
from frp.models import db
from flask import current_app
from frp.models import (User, UserAuth, Role, USER_STATUS, is_email_exists,
                        Organization, OrganizationInfo, OrganizationWork, Campaign, 
                        Donation, Comment, Memory)
from flask_user import current_user, login_required, roles_required
import datetime
from bs4 import BeautifulSoup

# Initial Configuration

def test_add_user(test_db, test_client):
    add_user()
    # Check Data Base
    user = User.query.filter_by(email='user@test.com').first()
    assert user!=None
    # Check Web
    x = login('user@test.com','12345',test_client)
    assert 'test user' in x.data


def test_add_campaign(test_db, test_client):
    add_campaign()
    # Check Data Base
    campaign = Campaign.query.filter_by(title='Test Campaign').first()
    assert campaign!=None
    # Check Web
    x = test_client.get("/campaign/"+str(campaign.id))
    assert 'Test Campaign'  in x.data

def test_add_donations(test_db, test_client):
    for i in range(1,6):
        donation = add_donation()
        x = test_client.get("/campaign/"+str(donation.campaign.id))
        soup = BeautifulSoup(x.data)
        assert int(soup.find('span',{'class':'percentFunded'}).text) == i*20
    assert 'Fully Funded Campaign' in x.data

def test_del_donations(test_db, test_client):
    donation = Donation.query.filter_by(identification="ABCDEF").first()
    campaign = donation.campaign
    i=5
    for donation in campaign.donations:
        i-=1
        db.session.delete(donation)
        db.session.commit()
        x = test_client.get("/campaign/"+str(campaign.id))
        soup = BeautifulSoup(x.data)
        assert int(soup.find('span',{'class':'percentFunded'}).text) == i*20



def login(email, password,test_client):
    return test_client.post('/user/sign-in', data=dict(
        email=email,
        password=password
        ), follow_redirects=True)

def add_user():
    user = User.query.filter_by(email='user@test.com').first()
    if user != None:
        return user
    user = User(
            status=USER_STATUS.ACTIVE, 
            email='user@test.com',
            first_name='test', 
            last_name='user', 
            active=True,
            address='XXX',
            contact_number='123456789',
            pan_number='XXYYZZ',
            confirmed_at=datetime.datetime.now())
    db.session.add(user)
    user_auth = UserAuth(password=app.user_manager.hash_password('12345'), 
            user=user, active=True)
    db.session.add(user_auth)
    db.session.commit()
    return user

def add_org():
    org = Organization.query.filter_by(title='Test Title').first()
    if org != None:
        return org
    user = add_user()
    org = Organization(title='Test Title', created_by=user)
    db.session.add(org)
    org_info = OrganizationInfo(
         org=org, email='info@example.com', category=2, status=1, address='123, Street 2',
         contact_number='99010201011', facebook='http://facebook.com/mirafra', 
         website='http://www.mirafra.com',
         has_80g_certificate='t', person1_name='Alok',
         person1_position='CEO', person1_email='kuchlous@gmail.com',
         person2_position='COO', person2_email='shyam@example.com',
         person1_phone='898923232328', person2_name='shyam',
         person2_phone='89323232899')
    db.session.add(org_info)

    work = OrganizationWork(organization=org, choice_id='3') 

    db.session.commit()
    return org

def add_campaign():
    campaign = Campaign.query.filter_by(title='Test Campaign').first()
    if campaign != None:
        return campaign
    
    user = add_user()
    org = add_org()
    campaign = Campaign(created_by=user, org=org,
            title='Test Campaign', description=' Test description', 
            who='Test who', impact='test impact',
            utilization='A very large impact', state="Haryana", city="Karnal", nbooks='100', nlic=0, languages="Hindi, Tamil",
            image="1.jpg", status="Approved",approved_at=datetime.datetime.now(),
            total_impact_on_children='2000', featured=False)
    db.session.add(campaign)
    db.session.commit()
    return campaign

def add_donation(amount=1000):
    campaign = add_campaign()
    donation = Donation(donor=campaign.created_by, campaign=campaign, amount=amount, confirmation=53499, 
            city="Bangalore", state="Karnataka", first_name="Sahil", identification="ABCDEF",
            identification_type="DL", ann_choice=False,
            tax_exemption_certificate=False)
    db.session.add(donation)
    db.session.commit()
    return donation

