# -*- coding: utf-8 -*-

import wtforms
import coaster
from .. import app
from .signup import (LANGUAGE_CHOICES, 
        STATES, ORG_WORK_CHOICES)
from ..models import (ORG_STATUS_CHOICES)

__all__ = ['FilterForm']

class FilterForm(wtforms.Form):
    languages = wtforms.SelectMultipleField(
            label='Languages',
            choices = LANGUAGE_CHOICES)
    states = wtforms.SelectMultipleField(
            label='States',
            choices = STATES)
    types = wtforms.SelectMultipleField(
            label='Types',
            choices = ORG_STATUS_CHOICES)
