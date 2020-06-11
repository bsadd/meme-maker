from django.db.models import Count
from rest_framework import serializers
from rest_framework.fields import Field

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

    react = serializers.CharField(source='react_name')

    class Meta:
        model = PostReact
        fields = ['react', 'user']
        read_only_fields = ('user',)


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    moderator = UserSerializer()
    keywords = KeywordSerializer(many=True)

    reacts = PostReactSerializer(source='postreact_set', many=True)
    # serializers.PrimaryKeyRelatedField(queryset=KeywordList.objects.all(), many=True, read_only=True)

    is_template = serializers.CharField(source='is_template_post')

    url_view = serializers.CharField(source='get_absolute_url')
    url_edit = serializers.CharField(source='get_absolute_edit_url')
    url_template = serializers.CharField(source='get_absolute_template_edit_url')

    react_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'caption', 'image', 'nviews', 'is_adult', 'is_violent',
                  'configuration_head', 'configuration_over', 'configuration_tail',
                  'approval_status', 'approval_details', 'time', 'moderator',
                  'template', 'is_template', 'author', 'keywords', 'reacts', 'react_count',
                  'url_view', 'url_edit', 'url_template']  # , 'comments'
        read_only_fields = ('id', 'nviews', 'approval_status', 'approval_details', 'moderator',
                            'is_template', 'author', 'reacts', 'react_count', 'url_view', 'url_edit', 'url_template')

    def get_react_count(self, post):
        from memesbd.utils_db import get_react_count_post
        return get_react_count_post(post.id)
