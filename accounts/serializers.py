from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField('api:user-detail', read_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'url', 'avatar']
        read_only_fields = ('is_active', 'is_staff', 'is_superuser')
        extra_kwargs = {
            'password': {'write_only': True}
        }
