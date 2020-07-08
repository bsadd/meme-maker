from django.utils import timezone
from drf_writable_nested import UniqueFieldsMixin, NestedUpdateMixin
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers, exceptions
from rest_framework_nested.relations import NestedHyperlinkedIdentityField

from coreapp.models import *
from accounts.serializers import UserSerializer
from coreapp.serializer_fields import ChoiceField, ImageBase64HybridFileField


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
                                         parent_lookup_kwargs={'post_pk': 'post_id'}, read_only=True,
                                         label="reaction's view url")

    class Meta:
        model = PostReact
        fields = ['react', 'user', 'post', 'url']

    def get_unique_together_validators(self):
        """disable unique together checks for (user, post) for get_or_create operation in create"""
        return []


class PostSerializer(NestedUpdateMixin, serializers.ModelSerializer):
    """
    TODO: optimize react count
    TODO:https://github.com/beda-software/drf-writable-nested/issues/46#issuecomment-415632868
    TODO: generic https://github.com/Ian-Foote/rest-framework-generic-relations
    """
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    publisher = serializers.SerializerMethodField()

    approval_status = ChoiceField(choices=ApprovalStatus.approval_status(), read_only=True)
    moderator = serializers.HyperlinkedRelatedField(view_name='api:user-detail', read_only=True)

    keywords = KeywordSerializer(many=True, required=False)
    image = ImageBase64HybridFileField()  # image file / base64

    reacts = serializers.HyperlinkedIdentityField(read_only=True, view_name='api:post-react-list',
                                                  lookup_url_kwarg='post_pk', help_text="all reactions for this post")

    template = serializers.HyperlinkedRelatedField(queryset=Post.approved.all(), view_name='api:post-detail',
                                                   required=False)  # Post.approved restricts unapproved as template ref
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='api:post-detail')

    is_template = serializers.BooleanField(source='is_template_post', read_only=True)

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
        read_only_fields = ('nviews', 'uploaded_at', 'approval_status', 'approval_details', 'approval_at', 'moderator',)
        extra_kwargs = {
            'caption': {'required': True},
            'image': {'required': True},
            'configuration_over': {'write_only': True},
            'configuration_head': {'write_only': True},
            'configuration_tail': {'write_only': True},
        }

    @swagger_serializer_method(serializer_or_field=serializers.DictField())
    def get_publisher(self, post) -> dict:
        """Returns uploader info
        :return {'username':current user name, 'url': user-profile link}
        """
        return {'username': post.author.username,
                'url': self.context['request'].build_absolute_uri(reverse('api:user-detail', args=[post.author_id]))}

    @swagger_serializer_method(serializer_or_field=serializers.DictField())
    def get_react_counts(self, post) -> dict:
        """Returns all reactions:count map for this post
        :return: {'WOW':10, 'HAHA':4}
        """
        # To skip db hit obj ref is used to query
        rset = {}
        for q in post.postreact_set.exclude(react=Reacts.NONE).values('react').annotate(
                count=Count('user')).values_list('react', 'count'):
            rset[Reacts.REACT_NAMES[q[0]]] = q[1]
        return rset

    @swagger_serializer_method(
        serializer_or_field=ChoiceField(choices=Reacts.react_choices(),
                                        help_text="name of reaction of current user"))
    def get_react_user(self, post):
        """Returns current user's reaction on this posts
        :return: reaction-name or null if no reaction from the user
        """
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
    template = serializers.HyperlinkedRelatedField(queryset=Post.approved.all(), view_name='api:post-detail',
                                                   required=False)

    class Meta:
        model = Post
        fields = ['id', 'caption', 'image', 'nviews', 'is_adult', 'is_violent', 'author',
                  'uploaded_at', 'approval_status', 'approval_details', 'approval_at', 'moderator',
                  'template', 'author', 'keywords', ]
        read_only_fields = ('caption', 'image', 'nviews', 'author', 'uploaded_at', 'moderator', 'keywords',)
        extra_kwargs = {}
