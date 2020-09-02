from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins, viewsets

from coreapp.models import Post
from coreapp.pagination import StandardResultsSetPagination
from coreapp.permissions import IsModerator
from coreapp.serializers.PostSerializers import PostModerationSerializer
from coreapp.swagger import query_params


@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(operation_summary='Moderation specific details of a post',
                                                manual_parameters=[
                                                    query_params.REQUIRED_MODERATION_AUTHORIZATION_PARAMETER],
                                                responses={status.HTTP_404_NOT_FOUND: 'Post not found/approved'}))
@method_decorator(name='list',
                  decorator=swagger_auto_schema(operation_summary='List of posts for moderation',
                                                manual_parameters=[
                                                    query_params.REQUIRED_MODERATION_AUTHORIZATION_PARAMETER]))
@method_decorator(name='update',
                  decorator=swagger_auto_schema(operation_summary='Update Post Moderation Status/Detail',
                                                manual_parameters=[
                                                    query_params.REQUIRED_MODERATION_AUTHORIZATION_PARAMETER],
                                                responses={status.HTTP_404_NOT_FOUND: 'Post not found'}))
class PostModerationViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    """
    API endpoint to allow moderators to approve/moderate posts
    """
    pagination_class = StandardResultsSetPagination
    serializer_class = PostModerationSerializer
    permission_classes = (IsModerator,)
    queryset = Post.objects.prefetch_related('reactions', 'user', 'moderator').all()
    http_method_names = ('get', 'post', 'put')