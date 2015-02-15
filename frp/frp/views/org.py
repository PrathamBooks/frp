# -*- coding: utf-8 -*-

from flask import (render_template,
                   g,
                   url_for,
                   redirect,
                   session,
                   flash,
                   views,
                   request)

from .. import app
from ..models import ORG_STATUS_CHOICES
from ..forms import BENEFICIARY_CATEGORY, ORG_WORK_CHOICES
from ..service.decorators import login_required


@app.route('/admin/orginfos')
@login_required
def org_info():
    orgs = g.user.organization_created
    return render_template(
        'org_info.html', orgs=orgs, work_choices=dict(ORG_WORK_CHOICES),
        category=dict(BENEFICIARY_CATEGORY), status=dict(ORG_STATUS_CHOICES))
