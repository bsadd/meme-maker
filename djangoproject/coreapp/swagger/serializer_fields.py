from drf_yasg import openapi
from rest_framework import serializers


class Post_reaction_counts(serializers.JSONField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "title": "Enum keyed Dictionary",
            "properties": {
                "Like": openapi.Schema(
                    title="Like-count",
                    type=openapi.TYPE_INTEGER,
                ),
                # "Love": 10,
                # "Haha": 10,
                # "Wow": 10,
                # "Sad": 10,
                # "Angry": 10,
            },
        }


class Post_publisher(serializers.JSONField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "title": "Dictionary",
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
            },
        }
