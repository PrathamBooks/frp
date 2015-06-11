import sys
import os
import pytest
from datetime import *
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../../frp/')

from frp import app, models
from frp.models import (db, User, UserAuth, Role, USER_STATUS, is_email_exists,
                        Organization, OrganizationInfo, OrganizationWork, Campaign, 
                        Donation, Comment, Memory)

@pytest.fixture
def seed_db():
    admin = Role(
            name="admin",
            description="Administrator who can approve campaigns"
            )
    db.session.add(admin)

    user = User(
            status=USER_STATUS.ACTIVE, 
            email='admin@example.com',
            first_name='Pratham', 
            last_name='Admin', 
            active=True,
            address='XXX',
            contact_number='123456789',
            pan_number='XXYYZZ',
            roles=[admin],
            confirmed_at=datetime.now())

    
    db.session.add(user)

    user_auth = UserAuth(password=app.user_manager.hash_password('admin123'), 
            user=user, active=True)
    db.session.add(user_auth)

    user = User(
            status=USER_STATUS.ACTIVE, 
            email='user1@example.com',
            first_name='User', 
            last_name='1', 
            active=True,
            address='101, Good Homes',
            contact_number='990232323232',
            pan_number='XXYYZZ',
            confirmed_at=datetime.now())
    db.session.add(user)

    user_auth = UserAuth(password=app.user_manager.hash_password('user1123'), 
            user=user, active=True)
    db.session.add(user_auth)

    org = Organization(title='Whitefield Awake', created_by=user)
    db.session.add(org)

    # Create org info
    org_info = OrganizationInfo(
         org=org, email='info@example.com', category=2, status=1, address='123, Street 2',
         contact_number='99010201011', facebook='http://facebook.com/mirafra', 
         website='http://www.mirafra.com',
         has_80g_certificate='t', person1_name='User 1',
         person1_position='CEO', person1_email='user1@gmail.com',
         person2_position='COO', person2_email='user2@example.com',
         person1_phone='898923232328', person2_name='shyam',
         person2_phone='89323232899')
    db.session.add(org_info)

    work = OrganizationWork(organization=org, choice_id='3') 

    campaign = Campaign(created_by=user, org=org,
            title='Harayana Library', description='Project to get 1000 books for Ramagondanhalli School', 
            who='We are an organization of volunteers', impact='This will raise funds to buy 1000 books for government schools',
            utilization='A very large impact', state="Haryana", city="Karnal", nbooks='1000', nlic=0, languages="Hindi, Tamil",
            image="1.jpg", status="Approved",approved_at=datetime.now()-timedelta(days=1),
            total_impact_on_children='2000', featured=False)
    donation = Donation(donor=user, campaign=campaign, amount=50000, confirmation=53499, 
            city="Bangalore", state="Karnataka", first_name="Sahil", identification="ABCDEF",
            identification_type="DL", ann_choice=False,
            tax_exemption_certificate=False)
    db.session.add(donation)
    db.session.add(campaign)

    campaign = Campaign(created_by=user, org=org,
            title='Rural Library With a very very very long name that should not be allowed', description='Project to set up a rural library', 
            who='We are an organization who works in rural AP', impact='This will raise funds to set up a new library.',
            utilization='Utilize to get books', state="Andhra Pradesh", city="Hyderabad", nbooks='500', nlic=2, languages="Telugu, English",
            image="2.jpg", status="Approved",approved_at=datetime.now()-timedelta(days=2),
            total_impact_on_children='1000', featured=True)
    db.session.add(campaign)
    donation = Donation(donor=user, campaign=campaign, amount=10000, confirmation=53499, 
            city="Bangalore", state="Karnataka", first_name="Sahil", identification="ABCDEF",
            identification_type="P", ann_choice=False,
            tax_exemption_certificate=True)
    db.session.add(donation)
    comment = Comment(comment_by=user, campaign_comment=campaign, comment="[Dummy Comment 1]")
    db.session.add(comment)

    campaign = Campaign(created_by=user, org=org,
            title='Urban Library', description='Project to get 750 books for old age home', 
            who='We are an organization of old people', impact='Make 100 old people happy',
            utilization='It will help a few old people smile', state="Karnataka", city="Dharwad", nbooks='100', nlic=0, languages="English, Tamil",
            image="3.jpg", status="Rejected",
            total_impact_on_children='500', featured=True)
    db.session.add(campaign)

    campaign = Campaign(created_by=user, org=org,
            title='Slum Library', description='Slum library in Dharavi, Mumbai', 
            who='We are an organization of volunteers', impact='Library for street children',
            utilization='Take children off the streets', state="Maharashtra", city="Mumbai", nbooks='10000', nlic=0, languages="Hindi, Punjabi",
            image="4.jpg", status="Approved",approved_at=datetime.now()-timedelta(days=3),
            total_impact_on_children='4000', featured=True)
    db.session.add(campaign)

    comment = Comment(comment_by=user, campaign_comment=campaign, comment="[Dummy Comment 1]")
    db.session.add(comment)

    campaign = Campaign(created_by=user, org=org,
            title='Karnataka Library', description='Project to get 1000 books for Sidhapura School', 
            who='We are an organization of volunteers', impact='This will raise funds to buy 1000 books for government schools',
            utilization='A very large impact', state="Karnataka", city="Bangalore", nbooks='1000', nlic=0, languages="Kannada, Tamil",
            image="5.jpg", status="Approved",approved_at=datetime.now()-timedelta(days=4),
            total_impact_on_children='200', featured=True)
    db.session.add(campaign)

    comment = Comment(comment_by=user, campaign_comment=campaign, comment="[Dummy Comment 3]")
    db.session.add(comment)
    comment = Comment(comment_by=user, campaign_comment=campaign, comment="[Dummy Comment 2]")
    db.session.add(comment)
    comment = Comment(comment_by=user, campaign_comment=campaign, comment="[Dummy Comment 1]")
    db.session.add(comment)

    campaign = Campaign(created_by=user, org=org,
            title='Harayana Village Library', description='Project to get 1000 books for Ramagondanhalli School', 
            who='We are an organization of volunteers', impact='This will raise funds to buy 1000 books for government schools',
            utilization='A very large impact', state="Haryana", city="Karnal", nbooks='1000', nlic=0, languages="Hindi, Tamil",
            image="6.jpg", status="Approved",approved_at=datetime.now()-timedelta(days=5),
            total_impact_on_children='1500', featured=False)
    db.session.add(campaign)


    campaign = Campaign(created_by=user, org=org,
            title='Varthur Village Library', description='Project to get 1000 books for Ramagondanhalli School', 
            who='We are an organization of volunteers', impact='This will raise funds to buy 1000 books for government schools',
            utilization='A very large impact', state="Haryana", city="Karnal", nbooks='1000', nlic=0, languages="Hindi, Tamil",
            image="6.jpg", status="Approved",approved_at=datetime.now()-timedelta(days=5),
            total_impact_on_children='1500', featured=False)
    db.session.add(campaign)


    campaign = Campaign(created_by=user, org=org,
            title='Ramgondahalli Village Library', description='Project to get 1000 books for Ramagondanhalli School', 
            who='We are an organization of volunteers', impact='This will raise funds to buy 1000 books for government schools',
            utilization='A very large impact', state="Haryana", city="Karnal", nbooks='1000', nlic=0, languages="Hindi, Tamil",
            image="6.jpg", status="Approved",approved_at=datetime.now()-timedelta(days=5),
            total_impact_on_children='1500', featured=False)
    db.session.add(campaign)

    memory = Memory(name="Alok", city="Bangalore", state="Karnataka", 
            email="alok@example.com", can_share=True, words="Hello there from Alok")
    db.session.add(memory)

    memory = Memory(name="Sai", city="Bangalore", state="Karnataka", 
            email="sai@example.com", can_share=False, words="Hello there from Sai")
    db.session.add(memory)

    db.session.commit()

def add_user():
    user = User(
            status=USER_STATUS.ACTIVE, 
            email='user@test.com',
            first_name='test', 
            last_name='user', 
            active=True,
            address='XXX',
            contact_number='123456789',
            pan_number='XXYYZZ',
            confirmed_at=datetime.now())
    db.session.add(user)
    user_auth = UserAuth(password=app.user_manager.hash_password('12345'), 
            user=user, active=True)
    db.session.add(user_auth)
    db.session.commit()
    return user

def add_org(user):
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

def add_campaign(user, org):
    campaign = Campaign(created_by=user, org=org,
            title='Test Campaign', description=' Test description', 
            who='Test who', impact='test impact',
            utilization='A very large impact', state="Haryana", city="Karnal", nbooks='100', nlic=0, languages="Hindi, Tamil",
            image="1.jpg", status="Approved",approved_at=datetime.now(),
            total_impact_on_children='2000', featured=False)
    db.session.add(campaign)
    db.session.commit()
    return campaign

def add_donation(campaign, amount=1000):
    donation = Donation(donor=campaign.created_by, campaign=campaign, amount=amount, confirmation=53499, 
            city="Bangalore", state="Karnataka", first_name="Sahil", identification="ABCDEF",
            identification_type="DL", ann_choice=False,
            tax_exemption_certificate=False)
    db.session.add(donation)
    db.session.commit()
    return donation

def login(email, password,test_client):
    return test_client.post('/user/sign-in', data=dict(
        email=email,
        password=password
        ), follow_redirects=True)

def logout(test_client):
    return test_client.post('/user/sign-out', follow_redirects=True)

@pytest.fixture
def test_db(request):
    # In case left behind from a hung test last time
    models.db.drop_all()
    app.config.from_pyfile("settings/test.py")
    models.db.create_all()
    def fin():
        models.db.drop_all()
    request.addfinalizer(fin)

@pytest.fixture
def test_client(request):
    app.config.from_pyfile("settings/test.py")
    tc = app.test_client()
    return tc
