from django.db import transaction
from django.utils import timezone
from drf_extra_fields import fields as extra_fields
from drf_writable_nested import UniqueFieldsMixin, NestedUpdateMixin
from rest_framework import serializers, exceptions
from rest_framework_nested.relations import NestedHyperlinkedIdentityField

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
    user = serializers.HyperlinkedRelatedField(queryset=User.objects.all(),
                                               view_name='api:user-detail',
                                               default=serializers.CurrentUserDefault())
    post = serializers.HyperlinkedRelatedField(queryset=Post.approved.all(), view_name='api:post-detail', required=True)
    react = ChoiceField(choices=Reacts.react_choices(), required=True)
    url = NestedHyperlinkedIdentityField(view_name='api:post-react-detail',
                                         parent_lookup_kwargs={'post_pk': 'post_id'}, read_only=True)

    class Meta:
        model = PostReact
        fields = ['react', 'user', 'post', 'url']
        read_only_fields = ('user',)

    def get_unique_together_validators(self):
        """disable unique together checks for (user, post) for get_or_create operation in create"""
        return []


class PostSerializer(NestedUpdateMixin, serializers.ModelSerializer):
    """
    TODO:https://github.com/beda-software/drf-writable-nested/issues/46#issuecomment-415632868
    TODO: generic https://github.com/Ian-Foote/rest-framework-generic-relations
    """
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    publisher = serializers.SerializerMethodField()

    approval_status = ChoiceField(choices=ApprovalStatus.approval_status(), read_only=True)
    moderator = serializers.HyperlinkedRelatedField(view_name='api:user-detail', read_only=True)

    keywords = KeywordSerializer(many=True, required=False)
    image = extra_fields.HybridImageField()  # image file / base64

    reacts = serializers.HyperlinkedIdentityField(read_only=True, view_name='api:post-react-list',
                                                  lookup_url_kwarg='post_pk')

    template = serializers.HyperlinkedRelatedField(queryset=Post.approved.all(), view_name='api:post-detail',
                                                   required=False)  # Post.approved restricts unapproved as template ref
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='api:post-detail')

    is_template = serializers.CharField(source='is_template_post', read_only=True)

    react_counts = serializers.SerializerMethodField()

    react_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'caption', 'image', 'nviews', 'is_adult', 'is_violent',
                  'configuration_head', 'configuration_over', 'configuration_tail',
                  'uploaded_at', 'approval_status', 'approval_details', 'approval_at', 'moderator',
                  'author', 'publisher', 'url',
                  'template', 'is_template', 'react_counts', 'react_user',  # , 'reacts'
                  'keywords', 'reacts',
                  ]
        read_only_fields = ('uploaded_at', 'approval_status', 'approval_details', 'approval_at', 'moderator',)
        extra_kwargs = {
            'caption': {'required': True},
            'image': {'required': True},
            'configuration_over': {'write_only': True},
            'configuration_head': {'write_only': True},
            'configuration_tail': {'write_only': True},
        }

    def get_publisher(self, post):
        return {'username': post.author.username,
                'url': self.context['request'].build_absolute_uri(reverse('api:user-detail', args=[post.author_id]))}

    def get_react_counts(self, post):
        return PostReact.objects.reacts_count_map(post_id=post.id)

    def get_react_user(self, post):
        try:
            request = self.context['request']
            post_react = post.postreact_set.all().without_removed_reacts().get(user_id=request.user.id)
            return post_react.react_name()
        except (PostReact.DoesNotExist, KeyError, TypeError):  # TypeError for Anonymous User
            return None

    @transaction.atomic
    def create(self, validated_data):
        try:
            keywords_data = validated_data.pop('keywords')
            keyword_names_given = [keyword['name'].lower() for keyword in keywords_data if keyword['name'] != '']
            keyword_names_given = sorted(set(keyword_names_given), key=lambda x: keyword_names_given.index(x))
            Keyword.objects.bulk_create([Keyword(name=name) for name in keyword_names_given], ignore_conflicts=True)
            keywords = Keyword.objects.filter(name__in=keyword_names_given).order_by('name')
            keyword_names_saved = sorted({keyword.name for keyword in keywords})
            if keyword_names_given != keyword_names_saved:
                raise exceptions.APIException(detail='could not save keyword in the database')
            return Post.objects.create(**validated_data, keywords=keywords)
        except KeyError:
            return Post.objects.create(**validated_data)


class PostModerationSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    moderator = UserSerializer(default=serializers.CurrentUserDefault())
    approval_at = serializers.DateTimeField(default=timezone.now())
    approval_status = ChoiceField(choices=ApprovalStatus.approval_status())
    keywords = KeywordSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'caption', 'image', 'nviews', 'is_adult', 'is_violent', 'author',
                  'uploaded_at', 'approval_status', 'approval_details', 'approval_at', 'moderator',
                  'template', 'author', 'keywords', ]
        read_only_fields = ('caption', 'image', 'nviews', 'author', 'uploaded_at', 'moderator', 'template', 'keywords',)
        extra_kwargs = {}
