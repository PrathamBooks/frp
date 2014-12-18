import json
from flask import g
from ..models import Campaign, db


def create_campaign_from_webform(data):
    campaign = Campaign(user_id=g.user.id, data=json.dumps(data))

    db.session.add(campaign)

    db.session.commit()

    return campaign


def get_campaign_rendering_data():
    camps = []
    for camp in Campaign.query.all():
        camp_dict = json.loads(camp.data)
        camp_dict['id'] = str(camp.id).zfill(3)
        camps.append(camp_dict)
    return camps


def get_campaign_preview_data(id):
    try:
        id = int(id)
    except:
        return None

    camp = Campaign.query.filter_by(id=id).first()

    camp_dict = json.loads(camp.data)
    camp_dict['id'] = camp.id
    if camp_dict.get('image_file_path'):
        camp_dict['image_file_path'] = '/static{}'.format(camp_dict.get('image_file_path').split('static')[-1])
    return camp_dict
