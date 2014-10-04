# -*- coding: utf-8 -*-

import inspect


__all__ = ['ORG_STATUS', 'ORG_STATUS_CHOICES']


def get_attrs(cls):
    attrs = inspect.getmembers(cls, lambda a: not(inspect.isroutine(a)))
    return [a for a in attrs if not(a[0].startswith('__') and
                                    a[0].endswith('__'))]


class ORG_STATUS:
    registered_non_profit = {'desc': 'Registered non-profit',
                             'value': 1}
    section_25_company = {'desc': 'Section 25 Company',
                          'value': 2}
    private_school = {'desc': 'Private School',
                      'value': 3}
    budget_private_school = {
        'desc': 'Budget Private School (fee structure less than Rs.500 per month)',
        'value': 4}
    government_school = {'desc': 'Government School',
                          'value': 5}
    reading_centre = {'desc': 'Reading centre / library',
                          'value': 6}


ORG_STATUS_CHOICES = sorted(map(lambda x: (x[1]['value'], x[1]['desc']),
                                get_attrs(ORG_STATUS)))
