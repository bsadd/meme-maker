from memesbd.consts_db import *
import six

from filters.schema import base_query_params_schema
from filters.validations import (
    CSVofIntegers,
    IntegerLike,
    DatetimeWithTZ
)


def is_valid_react(react):
    return Reacts.is_valid_react(react)


post_query_schema = base_query_params_schema.extend(
    {
        'uploader': CSVofIntegers(),
        'violent': six.text_type,
        'adult': six.text_type,
        'keyword': six.text_type,
        'uploaded-before': DatetimeWithTZ(),
        'uploaded-after': DatetimeWithTZ(),
        'uploaded-on': DatetimeWithTZ(),
    }
)
