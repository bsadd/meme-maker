from rest_framework import serializers

from memesbd.models import *
from accounts.serializers import UserSerializer


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'

    def to_representation(self, value):
        return value.name


class PostReactSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    # id = serializers.ReadOnlyField(source='post.id')

    # re = serializers.Field(source='post.name')

    class Meta:
        model = PostReact
        fields = ['react', 'user']

    # def to_representation(self, value):
    #     return value


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    moderator = UserSerializer()
    keywords = KeywordSerializer(many=True)

    reacts = PostReactSerializer(source='postreact_set', many=True)
    # serializers.PrimaryKeyRelatedField(queryset=KeywordList.objects.all(), many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'caption', 'image', 'nviews', 'is_adult',
                  'is_violent', 'configuration_head', 'configuration_over', 'configuration_tail', 'approval_status',
                  'approval_details', 'time', 'moderator', 'template', 'author', 'keywords', 'reacts']  # , 'comments'
        # [f.name for f in Post._meta.get_fields()]
        # ['id','caption','image_url','nviews','is_adult','is_adult']
