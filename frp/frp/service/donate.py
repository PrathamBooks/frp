from random import randint
from flask import g
from .. import app
from ..models import (db, Donation, admin_user)
from flask_user import current_user

def create_donation(form, campaign):
  amount = form.amount_choice.data
  if not amount:
    amount = form.customize_amount.data
  # in case the donor did not sign in, the donation is accounted for in
  # in admin account
  donor = current_user if current_user.is_active() else admin_user()
  if (ann_choice == True):
      ann_choice = 1
  else:
      ann_choice = 0
  confirmation = randint(1000000, 9999999)
  donation = Donation(amount=amount, 
          donor=donor, 
          first_name=form.first_name.data,
          last_name=form.last_name.data,
          campaign=campaign, 
          confirmation=confirmation, 
          state=form.state.data, 
          city=form.city.data, 
          identification=form.pan_number.data,
          ann_choice=form.ann_choice.data)
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


