from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        """TODO: limit fields"""
        model = User
        fields = ['username', 'first_name', 'last_name']  # , 'is_superuser', 'is_moderator'  # '__all__'
        read_only_fields = ('is_active', 'is_staff', 'is_superuser')
        extra_kwargs = {
            'password': {'write_only': True}
        }
