from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedIdentityField

from coreapp.consts_db import Reaction
from coreapp.models import PostReaction
from coreapp.serializers.serializer_fields import ChoiceField


class PostReactionRequestBodySerializer(serializers.ModelSerializer):
    reaction = ChoiceField(choices=Reaction.choices, required=True)

    class Meta:
        model = PostReaction
        fields = ['reaction']


class PostReactionResponseBodySerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='api:user-detail', read_only=True)
    post = serializers.HyperlinkedRelatedField(view_name='api:post-detail', read_only=True)
    reaction = ChoiceField(choices=Reaction.choices, read_only=True)
    url = NestedHyperlinkedIdentityField(view_name='api:post-reaction-detail',
                                         parent_lookup_kwargs={'post_pk': 'post_id'},
                                         label="reaction's view url")

    class Meta:
        model = PostReaction
        fields = ['reaction', 'user', 'post', 'url']
