from rest_framework import serializers
from drf_extra_fields import fields as extra_fields


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        return self._choices[obj]

    def to_internal_value(self, data):
        """Used while storing value for the field."""
        data = data.capitalize()
        for i in self._choices:
            if self._choices[i] == data:
                return i
        raise serializers.ValidationError("Acceptable values are {0}.".format(list(self._choices.values())))


class ImageBase64HybridFileField(extra_fields.HybridImageField):
    class Meta:
        swagger_schema_fields = {
            'type': 'string',
            'title': 'Image Base64 Content',
            'description': 'Content of the image as base64 encoded string or file itself',
            'help_text': 'Parses base64 encoded string of an image but returns image url',
            'read_only': False  # <-- FIX
        }
