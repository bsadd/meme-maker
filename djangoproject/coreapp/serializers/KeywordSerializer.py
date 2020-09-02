from drf_writable_nested import UniqueFieldsMixin
from rest_framework import serializers

from coreapp.models import Keyword


class KeywordSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ('name',)  # '__all__'

    def to_representation(self, value):
        """overridden to support returning of plain json array like [key1, key2]"""
        return value.name

    def to_internal_value(self, data):
        """overridden to also support parsing of plain json array like [key1, key2]"""
        if type(data) == str:
            return super().to_internal_value(data={'name': data})
        return super().to_internal_value(data)