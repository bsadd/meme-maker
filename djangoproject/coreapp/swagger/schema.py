from abc import ABCMeta

from drf_yasg import openapi
from rest_framework import serializers
from rest_framework import status

from coreapp.swagger import query_params


class AbstractListCreateSchema(metaclass=ABCMeta):
    """
    fill app_name with django app name, resource_name and resource_name_plural with
    singular and plural form of the resource. They combined create ID and description
    endpoints like /app_name/resource_name/
    list_query_params contains a list of query parameters for GET /app_name/resource_name/
    list_success_response_serializer is the serializer class for successful response this request
    create_request_body_serializer contains the serializer used to create the resource
    create_success_response_serializer (usually model_serializer with all fields) defines the
    serializer class for successful response.
    """

    @property
    def app_name(self):
        """ """
        pass

    @property
    def resource_name(self):
        """ fill this property with resource (model) name. It is used to generate ID """
        pass

    @property
    def resource_name_plural(self):
        """ fill this property with plural resource name. Used for description and ID """
        pass

    @property
    def list_success_response_serializer(self):
        pass

    # def list(self, desc=None, manual_param=None, list_query_params=None):
    #     if desc is None:
    #         desc = "gives a paginated list of {resource_name_plural}".format(
    #             resource_name_plural=self.resource_name_plural
    #         )
    #
    #     if list_query_params is not None:
    #         if manual_param is not None:
    #             manual_param.extend([*list_query_params])
    #         else:
    #             manual_param = [*list_query_params]
    #
    #     return {
    #         'operation_id': "{app_name}_list_{resource_name_plural}".format(
    #             app_name=self.app_name,
    #             resource_name_plural=self.resource_name_plural
    #         ),
    #         'operation_description': desc,
    #         'query_serializer': None,
    #         'manual_parameters': manual_param,
    #         'request_body': None,
    #         'responses': {
    #             '200': self.list_success_response_serializer,
    #             '401': status.HTTP_401_RESPONSE,
    #             '404': status.HTTP_404_NOT_FOUND
    #         },
    #     }
    #
    def create(self, operation_description=None, manual_parameters=None):
        if operation_description is None:
            operation_description = "create new {resource_name}".format(
                resource_name=self.resource_name
            )
        if manual_parameters is None:
            manual_parameters = [query_params.REQUIRED_AUTHORIZATION_PARAMETER]
        return {
            'operation_id': "{app_name}_create_{resource_name_plural}".format(
                app_name=self.app_name,
                resource_name_plural=self.resource_name_plural
            ),
            'operation_description': operation_description,
            # 'query_serializer': self.model_serializer,
            'manual_parameters': manual_parameters,
            # 'request_body': self.create_request_body_serializer,
            'responses': {
                '201': status.HTTP_201_CREATED,
                '400': status.HTTP_400_BAD_REQUEST,
                '401': status.HTTP_401_UNAUTHORIZED,
                '404': status.HTTP_404_NOT_FOUND,
            },
        }


class UserRefSerializerSchema(serializers.JSONField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "title": "UserReference",
            "properties": {
                "username": openapi.Schema(
                    title="Username",
                    type=openapi.TYPE_STRING,
                ),
                "url": openapi.Schema(
                    title="Profile-link",
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_URI,
                ),
                "avatar": openapi.Schema(
                    title="User-Avatar",
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_URI,
                ),
            },
        }
