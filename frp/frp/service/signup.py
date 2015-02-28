# -*- coding: utf-8 -*-
import os
from shutil import copyfile

from flask import g

from .. import app

from ..models import (db, User, UserInfo, USER_STATUS, is_email_exists,
                      Organization, OrganizationInfo, OrganizationWork, Campaign)
from ..helpers import file_extension

def create_beneficiary(form, filename):
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
    # org_intro = form.org_intro.data
    total_impact_on_children = form.total_impact_on_children.data
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
        person2_phone=person2_phone, 
        total_impact_on_children=total_impact_on_children)

    db.session.add(org_info)

    for choice in org_work:
    # Create org work
        work = OrganizationWork(organization=org, choice_id=choice)
        db.session.add(work)

    # Create campaign
    project_title = form.project_title.data
    project_description = form.project_description.data
    project_who_are_you = form.project_who_are_you.data
    project_impact = form.project_impact.data
    fund_utilization = form.fund_utilization.data
    nbooks = form.project_books.data
    nlic = form.project_lib_in_classroom.data
    state = form.project_state.data
    city = form.project_city.data
    languages = []
    if not form.language1.data == 'Select':
        languages.append(form.language1.data)
    if not form.language2.data == 'Select':
        languages.append(form.language2.data)
    if not form.language3.data == 'Select':
        languages.append(form.language3.data)
    languages = ','.join((l) for l in languages)

    campaign = Campaign(created_by=g.user, org=org,
            title=project_title, description=project_description, 
            who=project_who_are_you, impact=project_impact,
            utilization=fund_utilization, nbooks=nbooks, nlic=nlic,
            state=state, city=city, languages=languages, status='Submitted', image='xx.png')
    db.session.add(campaign)

    try:
        db.session.commit()
        extension = file_extension(filename)
        full_file_path = os.path.join(app.config['UPLOAD_DIRECTORY'], 'tmp', filename)
        new_file_name = str(campaign.id) + '.' + extension
        full_new_path = os.path.join(app.config['UPLOAD_DIRECTORY'], 'uploads', new_file_name)
        copyfile(full_file_path, full_new_path)
        campaign = Campaign.query.get(campaign.id)
        campaign.image = new_file_name
        db.session.add(campaign)
        db.session.commit()

    except Exception as e:
        print e
        app.logger.warning('Unable to save')
        db.session.rollback()
        return {'error': True, 'exc': e}

    return {'error': False,
            'campaign': campaign}


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
