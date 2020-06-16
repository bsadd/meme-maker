from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField('api:user-detail', read_only=True)

    class Meta:
        """TODO: limit fields"""
        model = User
        fields = ['username', 'first_name', 'last_name', 'url']
        read_only_fields = ('is_active', 'is_staff', 'is_superuser')
        extra_kwargs = {
            'password': {'write_only': True}
        }
