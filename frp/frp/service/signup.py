# -*- coding: utf-8 -*-
import os
from shutil import copyfile

from flask import g
from flask_user import current_user

from .. import app

from ..models import (db, User, UserAuth, USER_STATUS, is_email_exists,
                      Organization, OrganizationInfo, OrganizationWork, Campaign)
from ..helpers import file_extension


from rq import Queue
from rq.job import Job
import redis

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)
q = Queue(connection=conn)

def edit_beneficiary(campaign, form, filename):
    org = campaign.org
    info = org.info

    org.title = form.title.data
    db.session.add(org)

    info.category = form.category.data
    info.status = form.organization_status.data
    info.address = form.address.data
    info.contact_number = form.contact_number.data
    info.email = form.email.data
    info.website = form.website.data
    info.facebook = form.facebook.data
    info.twitter = form.twitter.data
    info.blog = form.blog.data
    info.has_80g_certificate = form.has_80g_certificate.data
    info.person1_name = form.person1_name.data
    info.person1_position = form.person1_position.data
    info.person1_email = form.person1_email.data
    info.person1_phone = form.person1_phone.data
    info.person2_name = form.person2_name.data
    info.person2_position = form.person2_position.data
    info.person2_email = form.person2_email.data
    info.person2_phone = form.person2_phone.data

    db.session.add(info)
    for choice in org.works:
        db.session.delete(choice)

    org_work = form.org_work.data
    for choice in org_work:
    # Create org work
        work = OrganizationWork(organization=org, choice_id=choice)
        db.session.add(work)

    campaign.title = form.project_title.data
    campaign.description = form.project_description.data
    campaign.who = form.project_who_are_you.data
    campaign.impact = form.project_impact.data
    campaign.utilization = form.fund_utilization.data
    campaign.nbooks = form.project_books.data if form.project_books.data else 0
    campaign.total_impact_on_children = form.total_impact_on_children.data
    campaign.nlic = form.project_lib_in_classroom.data if form.project_lib_in_classroom.data else 0
    campaign.state = form.project_state.data
    campaign.city = form.project_city.data
    languages = []

    if not form.language1.data == '':
        languages.append(form.language1.data)
    if not form.language2.data == '':
        languages.append(form.language2.data)
    if not form.language3.data == '':
        languages.append(form.language3.data)
    languages = ', '.join((l) for l in languages)

    campaign.languages = languages

    db.session.add(campaign)
    try:
        db.session.commit()
        extension = file_extension(filename)
        full_file_path = os.path.join(app.config['UPLOAD_DIRECTORY'], 'tmp', filename)
        new_file_name = str(campaign.id) + '.' + extension
        full_new_path = os.path.join(app.config['UPLOAD_DIRECTORY'], 'uploads', new_file_name)
        copyfile(full_file_path, full_new_path)
        full_new_path = os.path.join(app.config['UPLOAD_DIRECTORY'], 'size_1', new_file_name)
        copyfile(full_file_path, full_new_path)
        full_new_path = os.path.join(app.config['UPLOAD_DIRECTORY'], 'size_2', new_file_name)
        copyfile(full_file_path, full_new_path)
        campaign = Campaign.query.get(campaign.id)
        campaign.image = new_file_name
        db.session.add(campaign)
        db.session.commit()

        if (app.config['VERSION'] == 'production'):
            from .image_backup import save_image
            app.logger.warning('Trying to backup image')
            job = q.enqueue_call(
                func=save_image, 
                args=(os.path.join(app.config['UPLOAD_DIRECTORY'], 'uploads'),
                    new_file_name,), 
                result_ttl=5000
                )
            app.logger.warning('image save job id: ' + str(job.id))

    except Exception as e:
        app.logger.warning(e)
        app.logger.warning('Unable to save campaign')
        db.session.rollback()
        return {'error': True, 'exc': e}

    return {'error': False,
            'campaign': campaign}

def create_beneficiary(form, filename):
    category = form.category.data
    title = form.title.data
    status = form.organization_status.data
    address = form.address.data
    contact_number = form.contact_number.data
    email = form.email.data
    website = form.website.data
    facebook = form.facebook.data
    twitter = form.twitter.data
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
    org_work = form.org_work.data

    # Create organization
    org = Organization(title=title, created_by=current_user)
    db.session.add(org)
    # Create org info
    org_info = OrganizationInfo(
        org=org, email=email, category=category, status=status, address=address,
        contact_number=contact_number, facebook=facebook, twitter=twitter, blog=blog,
        website=website,
        has_80g_certificate=has_80g_certificate, person1_name=person1_name,
        person1_position=person1_position, person1_email=person1_email,
        person1_phone=person1_phone, person2_name=person2_name,
        person2_position=person2_position, person2_email=person2_email,
        person2_phone=person2_phone)

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
    nbooks = form.project_books.data if form.project_books.data else 0
    total_impact_on_children = form.total_impact_on_children.data
    nlic = form.project_lib_in_classroom.data if form.project_lib_in_classroom.data else 0
    state = form.project_state.data
    city = form.project_city.data
    languages = []

    if not form.language1.data == '':
        languages.append(form.language1.data)
    if not form.language2.data == '':
        languages.append(form.language2.data)
    if not form.language3.data == '':
        languages.append(form.language3.data)
    languages = ', '.join((l) for l in languages)

    campaign = Campaign(created_by=current_user, org=org,
            title=project_title, description=project_description, 
            who=project_who_are_you, impact=project_impact,
            utilization=fund_utilization, nbooks=nbooks, nlic=nlic,
            state=state, city=city, languages=languages, 
            status='Submitted', image='xx.png',
            total_impact_on_children=total_impact_on_children,
            featured=False)
    db.session.add(campaign)
    try:
        db.session.commit()
        extension = file_extension(filename)
        full_file_path = os.path.join(app.config['UPLOAD_DIRECTORY'], 'tmp', filename)
        new_file_name = str(campaign.id) + '.' + extension
        full_new_path = os.path.join(app.config['UPLOAD_DIRECTORY'], 'uploads', new_file_name)
        copyfile(full_file_path, full_new_path)
        full_new_path = os.path.join(app.config['UPLOAD_DIRECTORY'], 'size_1', new_file_name)
        copyfile(full_file_path, full_new_path)
        full_new_path = os.path.join(app.config['UPLOAD_DIRECTORY'], 'size_2', new_file_name)
        copyfile(full_file_path, full_new_path)
        campaign = Campaign.query.get(campaign.id)
        campaign.image = new_file_name
        db.session.add(campaign)
        db.session.commit()

        if (app.config['VERSION'] == 'production'):
            from .image_backup import save_image
            app.logger.warning('Trying to backup image')
            job = q.enqueue_call(
                func=save_image, 
                args=(os.path.join(app.config['UPLOAD_DIRECTORY'], 'uploads'),
                    new_file_name,), 
                result_ttl=5000
                )
            app.logger.warning('image save job id: ' + str(job.id))

    except Exception as e:
        app.logger.warning(e)
        app.logger.warning('Unable to save campaign')
        db.session.rollback()
        return {'error': True, 'exc': e}

    return {'error': False,
            'campaign': campaign}

import datetime

def create_donor_from_facebook(data):
    """Create a user and userauth object from facebook data.

    :param data: `dict` containing facebook details.
    """
    user =is_email_exists(data.get('email'))
    if user:
        return user
    # We don't set username for facebook users.
    user = User(
        status=USER_STATUS.ACTIVE, email=data.get('email'),
        confirmed_at=datetime.datetime.now(),
        active=True, first_name=data.get('first_name'),
        last_name=data.get('last_name'))
    db.session.add(user)

    user_auth = UserAuth(user=user, active=True)
    db.session.add(user_auth)

    db.session.commit()
    return user

def reopen(campaign):
    new_target = campaign.target() - campaign.total_donations()
    nbooks = int(round(new_target/40))
    new_campaign = Campaign(title=campaign.title,
                           user_id=campaign.user_id,
                           nbooks=nbooks,
                           nlic=0,
                           organization_id=campaign.organization_id,
                           description=campaign.description,
                           who=campaign.who,
                           impact=campaign.impact,
                           total_impact_on_children=campaign.total_impact_on_children,
                           utilization=campaign.utilization,
                           state=campaign.state,
                           city=campaign.city,
                           languages=campaign.languages,
                           image=campaign.image,
                           status="Approved",
                           featured=campaign.featured,
                           approved_at=datetime.datetime.now()
                           )
    db.session.add(new_campaign)
    try:
        db.session.commit()
    except Exception as e:
        app.logger.warning(e)
        app.logger.warning('Unable to save campaign')
        db.session.rollback()
        return {'error': True, 'exc': e}

    return {'error': False,
            'new_campaign': new_campaign}