from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedIdentityField

from accounts.models import User
from coreapp.consts_db import Reaction
from coreapp.models import Post, PostReaction
from coreapp.serializers.serializer_fields import ChoiceField


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