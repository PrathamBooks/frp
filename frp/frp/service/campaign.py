import json
from flask import g
from ..models import Campaign, db


def create_campaign_from_webform(data):
    campaign = Campaign(user_id=g.user.id, data=json.dumps(data))

    db.session.add(campaign)

    db.session.commit()

    return campaign


def get_campaign_rendering_data():
    return map(lambda obj: json.loads(obj.data), Campaign.query.all())
