from voluptuous import Invalid

import six

from filters.schema import base_query_params_schema
from filters.validations import (
    CSVofIntegers,
    IntegerLike,
    DatetimeWithTZ
)


def BooleanText(msg=None):
    '''
    Checks whether a value is:
        - int, or
        - long, or
        - float without a fractional part, or
        - str or unicode composed only of alphanumeric characters
    '''

    def fn(value):
        if str(value).lower() not in ('true', 'false'):
            raise Invalid(msg or (
                'Invalid input <{0}>; expected an boolean text: true/false'.format(value))
                          )
        else:
            return value

    return fn


post_query_schema = base_query_params_schema.extend(
    {
        'uploader': CSVofIntegers(),
        'violent': BooleanText(),
        'adult': BooleanText(),
        'keyword': six.text_type,
        'uploaded-before': DatetimeWithTZ(),
        'uploaded-after': DatetimeWithTZ(),
        'uploaded-on': DatetimeWithTZ(),
    }
)
