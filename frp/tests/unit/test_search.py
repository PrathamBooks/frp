from frp.models import db
from frp.models import (User, UserAuth, Role, USER_STATUS, is_email_exists,
                        Organization, OrganizationInfo, OrganizationWork, Campaign, 
                        Donation, Comment, Memory)
from BeautifulSoup import BeautifulSoup

def test_search_shows_only_active_and_closed_campaigns(test_db, seed_db, test_client):
    campaigns = Campaign.query.search('hindi').all()
    for campaign in campaigns:
        assert campaign.status == 'Approved' or campaign.status == 'Closed'

