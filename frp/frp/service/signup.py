# -*- coding: utf-8 -*-

from ..models import db, User, UserInfo, USER_STATUS, is_email_exists


def create_donor_from_webform(donor):
    """Given an `forms.signup.DonorSignupForm` object create user and userinfo
    object.

    :param donor `forms.signup.DonorSignupForm`: donor form object.
    """
    user = User(
        status=USER_STATUS.INVITED, email=donor.email.data,
        password=donor.password.data, _username=donor.user_name.data)
    db.session.add(user)

    user_info = UserInfo(
        user=user, first_name=donor.first_name.data,
        last_name=donor.last_name.data, address=donor.address.data,
        contact_number=donor.contact_number.data,
        pan_number=donor.pan_number.data)
    db.session.add(user_info)

    # TODO: Send user activation email
    db.session.commit()


def create_donor_from_facebook(data):
    """Create a user and userinfo object from facebook data.

    :param data: `dict` containing facebook details.
    """
    if is_email_exists(data.get('email')):
        return
    # We don't set username for facebook users.
    user = User(
        status=USER_STATUS.ACTIVE, email=data.get('email'),)
    db.session.add(user)

    user_info = UserInfo(
        user=user, first_name=data.get('first_name'),
        last_name=data.get('last_name'),)
    db.session.add(user_info)

    db.session.commit()
