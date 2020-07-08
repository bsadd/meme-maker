from drf_yasg import openapi


def get_query_param(name, description, type):
    """ Gives a query parameter with given name, description and type """
    return openapi.Parameter(
        name=name,
        in_=openapi.IN_QUERY,
        description=description,
        type=type,
    )


def get_query_param_array(name, description, type):
    """ Gives a query parameter with given name, description and type """
    return openapi.Parameter(
        name=name,
        in_=openapi.IN_QUERY,
        description=description,
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(type=type)
    )


def get_authorization_param(required):
    return openapi.Parameter(
        name='Authorization',
        description='Token Authentication format: "Token <token-key>"',
        required=required,
        type=openapi.TYPE_STRING,
        in_=openapi.IN_HEADER
    )


POST_LIST_QUERY_PARAMS = [
    get_query_param_array('keyword', 'list of keywords (optional)', openapi.TYPE_STRING),
    get_query_param_array('uploader', 'uploader ids (optional)', openapi.TYPE_INTEGER),
    get_query_param('violent', 'violent posts only (optional)', openapi.TYPE_BOOLEAN),
    get_query_param('adult', 'adult posts only (optional)', openapi.TYPE_BOOLEAN),
    get_query_param('template', 'posts created from the given template id only (optional)', openapi.TYPE_INTEGER),
    get_query_param('uploaded-before', 'posts uploaded before the date (optional)', openapi.FORMAT_DATE),
    get_query_param('uploaded-after', 'posts uploaded after the date (optional)', openapi.FORMAT_DATE),
    get_query_param('uploaded-on', 'posts uploaded on the date (optional)', openapi.FORMAT_DATE),
]

USER_QUERY_PARAMETER = get_query_param('user', 'uuid of the user (optional)', openapi.TYPE_STRING)

REQUIRED_AUTHORIZATION_PARAMETER = get_authorization_param(required=True)
OPTIONAL_AUTHORIZATION_PARAMETER = get_authorization_param(required=False)
