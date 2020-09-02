from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins, viewsets

from coreapp.models import PostComment
from coreapp.permissions import IsAuthenticatedCreateOrOwnerModifyOrReadOnly
from coreapp.serializers.PostCommentSerializers import PostCommentCreateSerializer, PostCommentUpdateSerializer
from coreapp.swagger import query_params


@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(operation_summary='Details of a comment',
                                                responses={status.HTTP_404_NOT_FOUND: 'Comment not found'}))
@method_decorator(name='create',
                  decorator=swagger_auto_schema(operation_summary='New comment on the post',
                                                manual_parameters=[query_params.REQUIRED_AUTHORIZATION_PARAMETER],
                                                responses={status.HTTP_404_NOT_FOUND: 'Post not found/approved'}))
@method_decorator(name='update',
                  decorator=swagger_auto_schema(operation_summary='Modify an existing User Comment by owner',
                                                manual_parameters=[query_params.REQUIRED_AUTHORIZATION_PARAMETER],
                                                responses={status.HTTP_404_NOT_FOUND: 'Post/Comment not found'}))
class CommentViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    serializer_classes = {'retrieve': PostCommentCreateSerializer,
                          'create': PostCommentCreateSerializer,
                          'update': PostCommentUpdateSerializer, }
    permission_classes = (IsAuthenticatedCreateOrOwnerModifyOrReadOnly,)
    queryset = PostComment.objects.prefetch_related('user').all()
    http_method_names = ('get', 'post', 'put')

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, PostCommentCreateSerializer)