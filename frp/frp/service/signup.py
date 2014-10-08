# -*- coding: utf-8 -*-

from flask import g

from ..models import (db, User, UserInfo, USER_STATUS, is_email_exists,
                      Organization, OrganizationInfo, OrganizationWork)


def create_beneficary(form):
    category = form.category.data
    title = form.title.data
    status = form.organization_status.data
    address = form.address.data
    contact_number = form.contact_number.data
    email = form.email.data
    website = form.website.data
    facebook = form.facebook.data
    blog = form.blog.data
    has_80g_certificate = form.has_80g_certificate.data
    person1_name = form.person1_name.data
    person1_position = form.person1_position.data
    person1_email = form.person1_email.data
    person1_phone = form.person1_phone.data
    person2_name = form.person2_name.data
    person2_position = form.person2_position.data
    person2_email = form.person2_email.data
    person2_phone = form.person2_phone.data
    org_intro = form.org_intro.data
    total_impact_on_children = form.total_impact_on_children.data
    age_group_of_children = form.age_group_of_children.data
    org_work = form.org_work.data

    # Create organization
    org = Organization(title=title, created_by=g.user)
    db.session.add(org)
    # Create org info
    org_info = OrganizationInfo(
        org=org, email=email, category=category, status=status, address=address,
        contact_number=contact_number, facebook=facebook, blog=blog,
        website=website,
        has_80g_certificate=has_80g_certificate, person1_name=person1_name,
        person1_position=person1_position, person1_email=person1_email,
        person1_phone=person1_phone, person2_name=person2_name,
        person2_position=person2_position, person2_email=person2_email,
        person2_phone=person2_phone, intro=org_intro,
        total_impact_on_children=total_impact_on_children,
        age_group_of_children=age_group_of_children)
    db.session.add(org_info)

    # Create org work
    for choice in org_work:
        work = OrganizationWork(organization=org, choice_id=choice)
        db.session.add(work)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {'error': True, 'exc': e}

    return {'error': False}


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
