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

@pytest.fixture
def seed_db(request):
    user = add_user()
    org = add_org(user=user)
    campaign = add_campaign(user=user, org=org)
 
