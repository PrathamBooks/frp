from random import randint
from flask import g
from .. import app
from ..models import (db, User, UserInfo, USER_STATUS, is_email_exists,
                      Organization, OrganizationInfo, OrganizationWork, Campaign)

def donate(form):
  amount = form.amount.data
  donor = g.user
  campaign = Campaign.query.find(form.campaign.data)
  confirmation = randint(1000000, 9999999)
  donation = Donation(amount=amount, donor=donor, campaign=campaign, confirmation=confirmation)
  db.session.add(donation)
  try:
    db.session.commit()
  except Exception as e:
    print e
    app.logger.warning('Unable to save')
    db.session.rollback()
    return {'error': True, 'exc': e}
  return {'error': False,
          'donation': donation}


