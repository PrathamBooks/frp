# -*- coding: utf-8 -*-

from flask import session, g

from ..models import User, db


def get_user_dict():
    return {"is_staff": g.user.is_staff}


def is_valid_login(email, password):
    """If the username and password hash is matched `g.user` is set else
    False is returned.

    :param email `str`: Email id of the user.
    :param password `str`: Password of the user.
    """
    user = User.query.filter_by(email=email).first()
    if not user:
        return False

    if user.password_is(password):
        session['logged_in'] = True
        session['email'] = user.email
        return True

    return False


def update_profile(profile):
    """Update the profile.

    :param profile `forms.user.ProfileForm`: Form object with data.
    """
    user = g.user
    user.username = profile.user_name.data
    user.userinfo.first_name = profile.first_name.data
    user.userinfo.last_name = profile.last_name.data
    user.userinfo.address = profile.address.data
    user.userinfo.contact_number = profile.contact_number.data
    user.userinfo.pan_number = profile.pan_number.data
    user.userinfo.need_80g_certificate = profile.need_80g_certificate.data
    db.session.add(user)
    db.session.commit()
    return True
