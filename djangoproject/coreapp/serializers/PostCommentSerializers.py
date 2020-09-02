from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers, exceptions
from rest_framework.utils.serializer_helpers import ReturnDict

from accounts.serializers import UserRefSerializer
from coreapp.models import PostComment, Post
from coreapp.swagger.schema import UserRefSerializerSchema


class PostCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = PostComment

    @swagger_serializer_method(serializer_or_field=UserRefSerializerSchema)
    def get_user(self, postcomment) -> ReturnDict:
        return UserRefSerializer(postcomment.user, context=self.context).data


class PostCommentCreateSerializer(PostCommentSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.approved.all(), write_only=True, required=False)

    class Meta(PostCommentSerializer.Meta):
        fields = ('id', 'comment', 'created_at', 'parent',
                  'user', 'post')
        read_only_fields = (
            'created_at', 'user',)

    def create(self, validated_data):
        post = validated_data.get('post', None)
        parent = validated_data.get('parent', None)
        if post and parent:
            raise exceptions.ValidationError(detail='Only one of `post` or `parent` field can be passed')
        elif parent:
            post_id = parent.post_id
            return PostComment.objects.create(**validated_data, post_id=post_id, user=self.context['request'].user)
        elif post:
            return PostComment.objects.create(**validated_data, user=self.context['request'].user)
        else:
            raise exceptions.ValidationError(detail='Either `post` or `parent` field must be passed')


class PostCommentUpdateSerializer(PostCommentSerializer):
    class Meta(PostCommentSerializer.Meta):
        fields = ('id', 'comment', 'created_at', 'parent',
                  'user')
        read_only_fields = (
            'created_at', 'user', 'parent',)