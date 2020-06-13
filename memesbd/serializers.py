from django.db.models import Count
from drf_writable_nested import UniqueFieldsMixin, NestedUpdateMixin
from rest_framework import serializers
from rest_framework.fields import Field

from memesbd.models import *
from accounts.serializers import UserSerializer


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        return self._choices[obj]

    def to_internal_value(self, data):
        """Used while storing value for the field."""
        for i in self._choices:
            if self._choices[i] == data:
                return i
        raise serializers.ValidationError("Acceptable values are {0}.".format(list(self._choices.values())))


class KeywordSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
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


class PostSerializer(NestedUpdateMixin, serializers.ModelSerializer):
    """
    TODO:https://github.com/beda-software/drf-writable-nested/issues/46#issuecomment-415632868
    TODO: generic https://github.com/Ian-Foote/rest-framework-generic-relations
    """
    author = UserSerializer(default=serializers.CurrentUserDefault())
    approval_status = ChoiceField(choices=ApprovalStatus.approval_status(), read_only=True)
    moderator = UserSerializer(read_only=True)
    keywords = KeywordSerializer(many=True)

    # reacts = PostReactSerializer(source='postreact_set', many=True)

    is_template = serializers.CharField(source='is_template_post', required=False)

    react_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'caption', 'image', 'nviews', 'is_adult', 'is_violent',
                  'configuration_head', 'configuration_over', 'configuration_tail',
                  'uploaded_at', 'approval_status', 'approval_details', 'approval_at', 'moderator',
                  'template', 'is_template', 'author', 'react_count',  # , 'reacts'
                  'keywords', ]
        read_only_fields = ('uploaded_at', 'approval_status', 'approval_details', 'approval_at', 'moderator',)
        extra_kwargs = {
            'caption': {'required': True},
        }

    def get_react_count(self, post):
        from memesbd.utils_db import get_react_count_post
        return get_react_count_post(post.id)

    def create(self, validated_data):
        keywords_data = validated_data.pop('keywords')
        post = Post.objects.create(**validated_data)
        for keyword_data in keywords_data:
            keyword, _ = Keyword.objects.get_or_create(**keyword_data)
            KeywordList.objects.get_or_create(post=post, keyword=keyword)
        return post
