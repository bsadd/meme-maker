from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedIdentityField

from coreapp.consts_db import Reacts
from coreapp.models import PostReact
from coreapp.serializers import ChoiceField


class PostReactRequestBodySerializer(serializers.ModelSerializer):
    react = ChoiceField(choices=Reacts.react_choices(), required=True)

    class Meta:
        model = PostReact
        fields = ['react']


class PostReactResponseBodySerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='api:user-detail', read_only=True)
    post = serializers.HyperlinkedRelatedField(view_name='api:post-detail', read_only=True)
    react = ChoiceField(choices=Reacts.react_choices(), read_only=True)
    url = NestedHyperlinkedIdentityField(view_name='api:post-react-detail',
                                         parent_lookup_kwargs={'post_pk': 'post_id'},
                                         label="reaction's view url")

    class Meta:
        model = PostReact
        fields = ['react', 'user', 'post', 'url']
