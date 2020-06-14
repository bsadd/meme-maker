from django.db import transaction
from django.db.models import Count
from drf_extra_fields import fields as extra_fields
from drf_writable_nested import UniqueFieldsMixin, NestedUpdateMixin
from rest_framework import serializers
from rest_framework import exceptions
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
        fields = ('name',)  # '__all__'

    # def to_representation(self, value):
    #     return value.name


class PostReactSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # UserSerializer()

    react = ChoiceField(choices=Reacts.react_choices(), required=True)

    class Meta:
        model = PostReact
        fields = ['react', 'user', 'post']
        read_only_fields = ('user',)

    def get_unique_together_validators(self):
        """disable unique together checks for (user, post) for get_or_create operation in create"""
        return []

    def create(self, validated_data):
        react = validated_data.pop('react')
        post = validated_data.pop('post')
        if post.approval_status != ApprovalStatus.APPROVED:
            raise exceptions.ValidationError(detail='Post is not approved')
        post_react, _ = PostReact.objects.get_or_create(**validated_data, post=post)
        if post_react.react != react:
            post_react.react = react
            post_react.save()
        return post_react


class PostSerializer(NestedUpdateMixin, serializers.ModelSerializer):
    """
    TODO:https://github.com/beda-software/drf-writable-nested/issues/46#issuecomment-415632868
    TODO: generic https://github.com/Ian-Foote/rest-framework-generic-relations
    """
    author = UserSerializer(default=serializers.CurrentUserDefault())
    approval_status = ChoiceField(choices=ApprovalStatus.approval_status(), read_only=True)
    moderator = UserSerializer(read_only=True)
    keywords = KeywordSerializer(many=True, required=False)
    image = extra_fields.HybridImageField()  # image file / base64

    # reacts = PostReactSerializer(source='postreact_set', many=True)

    is_template = serializers.CharField(source='is_template_post', read_only=True)

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
            'image': {'required': True},
        }

    def get_react_count(self, post):
        from memesbd.utils_db import get_react_count_post
        return get_react_count_post(post.id)

    @transaction.atomic
    def create(self, validated_data):
        try:
            keywords_data = validated_data.pop('keywords')
            post = Post.objects.create(**validated_data)
            for keyword_data in keywords_data:
                keyword, _ = Keyword.objects.get_or_create(**keyword_data)
                KeywordList.objects.get_or_create(post=post, keyword=keyword)
            return post
        except KeyError:
            return Post.objects.create(**validated_data)
