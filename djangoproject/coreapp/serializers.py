from django.utils import timezone
from drf_writable_nested import UniqueFieldsMixin, NestedUpdateMixin
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers, exceptions
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework_nested.relations import NestedHyperlinkedIdentityField

from coreapp.models import *
from accounts.serializers import UserRefSerializer
from coreapp.serializer_fields import ChoiceField, ImageBase64HybridFileField
from coreapp.swagger.schema import UserRefSerializerSchema
from coreapp.swagger.serializer_fields import *


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


class PostReactionSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(queryset=User.objects.all(),
                                               view_name='api:user-detail',
                                               default=serializers.CurrentUserDefault())
    post = serializers.HyperlinkedRelatedField(queryset=Post.approved.all(), view_name='api:post-detail', required=True)
    reaction = ChoiceField(choices=Reaction.choices, required=True)
    url = NestedHyperlinkedIdentityField(view_name='api:post-reaction-detail',
                                         parent_lookup_kwargs={'post_pk': 'post_id'}, read_only=True,
                                         label="reaction's view url")

    class Meta:
        model = PostReaction
        fields = ['reaction', 'user', 'post', 'url']

    def get_unique_together_validators(self):
        """disable unique together checks for (user, post) for get_or_create operation in manager.create"""
        return []


class PostSerializer(NestedUpdateMixin, serializers.ModelSerializer):
    """
    TODO: optimize reaction count
    TODO:https://github.com/beda-software/drf-writable-nested/issues/46#issuecomment-415632868
    TODO: generic https://github.com/Ian-Foote/rest-framework-generic-relations
    """
    user = serializers.SerializerMethodField(read_only=True)

    approval_status = ChoiceField(choices=ApprovalStatus.choices, read_only=True)
    moderator = serializers.HyperlinkedRelatedField(view_name='api:user-detail', read_only=True)

    keywords = KeywordSerializer(many=True, required=False,
                                 help_text='Returns plain json array like, `keywords: ["key1", "key2"]` '
                                           'but parses either `keywords: ["key1"]` or `keywords: [{"name": "key1"}]`')
    image = ImageBase64HybridFileField()  # image file / base64

    reactions = serializers.HyperlinkedIdentityField(read_only=True, view_name='api:post-reaction-list',
                                                     lookup_url_kwarg='post_pk',
                                                     help_text="all reactions for this post")

    template = serializers.HyperlinkedRelatedField(queryset=Post.approved.all(), view_name='api:post-detail',
                                                   required=False)  # Post.approved restricts unapproved as template ref
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='api:post-detail')

    is_template = serializers.BooleanField(source='is_template_post', read_only=True)

    reaction_counts = serializers.SerializerMethodField()

    reaction_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'caption', 'image', 'nviews', 'is_adult', 'is_violent',
                  'configuration_head', 'configuration_over', 'configuration_tail',
                  'uploaded_at', 'approval_status', 'approval_details', 'approval_at', 'moderator',
                  'user', 'url',
                  'template', 'is_template', 'reaction_counts', 'reaction_user',
                  'keywords', 'reactions',
                  ]
        read_only_fields = ('nviews', 'uploaded_at', 'approval_status', 'approval_details', 'approval_at', 'moderator',)
        extra_kwargs = {
            'caption': {'required': True},
            'image': {'required': True},
            'configuration_over': {'write_only': True},
            'configuration_head': {'write_only': True},
            'configuration_tail': {'write_only': True},
        }

    @swagger_serializer_method(serializer_or_field=UserRefSerializerSchema)
    def get_user(self, post) -> ReturnDict:
        return UserRefSerializer(post.user, context=self.context).data

    @swagger_serializer_method(serializer_or_field=Post_reaction_counts)
    def get_reaction_counts(self, post) -> dict:
        """Returns all reactions:count map for this post
        :return: {'WOW':10, 'HAHA':4}
        """
        # To skip db hit obj ref is used to query
        rset = {}
        for q in post.postreaction_set.exclude(reaction=Reaction.NONE).values('reaction').annotate(
                count=Count('user')).values_list('reaction', 'count'):
            rset[Reaction(q[0]).label] = q[1]
        return rset

    @swagger_serializer_method(serializer_or_field=ChoiceField(choices=Reaction.choices,
                                                               help_text="name of reaction of current user"))
    def get_reaction_user(self, post):
        """Returns current user's reaction on this posts
        :return: reaction-name or null if no reaction from the user
        """
        try:
            request = self.context['request']
            post_reaction = post.postreaction_set.all().without_removed_reactions().get(user_id=request.user.id)
            return post_reaction.reaction_name()
        except (PostReaction.DoesNotExist, KeyError, TypeError):  # TypeError for Anonymous User
            return None

    @transaction.atomic
    def create(self, validated_data):
        """create is overridden to support update_or_create for list of keywords"""
        try:
            keywords_data = validated_data.pop('keywords')
            keyword_names_given = [keyword['name'].lower() for keyword in keywords_data if keyword['name'] != '']
            keyword_names_given = sorted(set(keyword_names_given), key=lambda x: keyword_names_given.index(x))
            Keyword.objects.bulk_create([Keyword(name=name) for name in keyword_names_given], ignore_conflicts=True)
            keywords = Keyword.objects.filter(name__in=keyword_names_given).order_by('name')
            keyword_names_saved = sorted({keyword.name for keyword in keywords})
            if keyword_names_given != keyword_names_saved:
                raise exceptions.APIException(detail='could not save keyword in the database')
            return Post.objects.create(**validated_data, keywords=keywords, user=self.context['request'].user)
        except KeyError:
            return Post.objects.create(**validated_data, user=self.context['request'].user)


class PostModerationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    moderator = serializers.SerializerMethodField(read_only=True)
    approval_at = serializers.DateTimeField(read_only=True)
    approval_status = ChoiceField(choices=ApprovalStatus.choices)
    keywords = KeywordSerializer(many=True, read_only=True)
    template = serializers.HyperlinkedRelatedField(view_name='api:post-detail', read_only=True)

    @swagger_serializer_method(serializer_or_field=UserRefSerializerSchema)
    def get_moderator(self, post):
        """TODO: need a better way
        https://github.com/axnsan12/drf-yasg/issues/343
        https://github.com/axnsan12/drf-yasg/issues/344
        """
        return UserRefSerializer(post.user, context=self.context).data

    @swagger_serializer_method(serializer_or_field=UserRefSerializerSchema)
    def get_user(self, post):
        return UserRefSerializer(post.moderator, context=self.context).data

    class Meta:
        model = Post
        fields = ['id', 'caption', 'image', 'nviews', 'is_adult', 'is_violent', 'user',
                  'uploaded_at', 'approval_status', 'approval_details', 'approval_at',
                  'moderator',
                  'template', 'user', 'keywords', ]
        read_only_fields = (
            'caption', 'image', 'nviews', 'user', 'uploaded_at', 'keywords', 'moderated_at',)
        extra_kwargs = {}

    def update(self, instance, validated_data):
        """update is overridden to set moderator and approval modification time"""
        instance.moderator = self.context['request'].user
        instance.approval_at = timezone.now()
        return super().update(instance, validated_data)


class PostCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = PostComment

    @swagger_serializer_method(serializer_or_field=UserRefSerializerSchema)
    def get_user(self, postcomment) -> ReturnDict:
        return UserRefSerializer(postcomment.user, context=self.context).data

    def create(self, validated_data):
        return PostComment.objects.create(**validated_data, user=self.context['request'].user)


class PostCommentCreateSerializer(PostCommentSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.approved.all(), write_only=True, required=True)

    class Meta(PostCommentSerializer.Meta):
        fields = ('id', 'comment', 'created_at', 'parent',
                  'user', 'post')
        read_only_fields = (
            'created_at', 'user',)


class PostCommentUpdateSerializer(PostCommentSerializer):
    class Meta(PostCommentSerializer.Meta):
        fields = ('id', 'comment', 'created_at', 'parent',
                  'user')
        read_only_fields = (
            'created_at', 'user', 'parent',)
