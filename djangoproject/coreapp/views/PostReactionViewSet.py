from django.urls import reverse
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins, viewsets, permissions, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response

from coreapp.consts_db import ApprovalStatus
from coreapp.models import PostReaction, Post
from coreapp.serializers.PostReactionSerializer import PostReactionSerializer
from coreapp.swagger import query_params
from coreapp.swagger.serializers import PostReactionRequestBodySerializer, PostReactionResponseBodySerializer


@method_decorator(name='list',
                  decorator=swagger_auto_schema(operation_summary="All reactions on a post",
                                                operation_description="All reactions on the post with post_id=post_pk",
                                                responses={status.HTTP_404_NOT_FOUND: 'Post not found/approved'}))
@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(operation_summary="Details of a reaction on a post",
                                                operation_description='Details of a reaction with reaction_id=id'
                                                                      ' on the post with post_id=post_pk',
                                                responses={status.HTTP_404_NOT_FOUND: 'Post not found/approved'}))
class PostReactionViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    """
    API endpoint that allows users to react or view reactions on approved posts.
    """
    serializer_class = PostReactionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        qs = PostReaction.objects.all().of_approved_posts()
        if 'post_pk' in self.kwargs:
            qs = qs.of_post(self.kwargs['post_pk'])
        return qs

    @swagger_auto_schema(method='get', operation_summary="Current user's reaction on the post",
                         manual_parameters=[query_params.REQUIRED_AUTHORIZATION_PARAMETER],
                         responses={status.HTTP_404_NOT_FOUND: 'Post/Reaction Not found'})
    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated],
            url_path='user', url_name='user')
    def user(self, request, post_pk=None):
        """
        currently authenticated user's reaction only on post with id=post_pk
        """
        try:
            post = Post.objects.get(id=post_pk, approval_status=ApprovalStatus.APPROVED)
            return Response(PostReactionSerializer(PostReaction.objects.get(post=post, user=request.user),
                                                   context={'request': request}).data,
                            status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            raise exceptions.NotFound(detail="No such react-able post exists with this id")
        except PostReaction.DoesNotExist:
            raise exceptions.NotFound(detail="No reaction on the post from this user")

    @swagger_auto_schema(request_body=PostReactionRequestBodySerializer,
                         operation_summary="Create/Change/Remove current user's reaction on the post by post-ID",
                         manual_parameters=[query_params.REQUIRED_AUTHORIZATION_PARAMETER],
                         responses={status.HTTP_201_CREATED: PostReactionResponseBodySerializer,
                                    status.HTTP_401_UNAUTHORIZED: 'User not authorized',
                                    status.HTTP_400_BAD_REQUEST: 'post/user passed in request body',
                                    status.HTTP_404_NOT_FOUND: 'Post Not found'})
    def create(self, request, *args, **kwargs):
        is_mutable = True if getattr(request.data, '_mutable', True) else request.data._mutable
        if not is_mutable:
            request.data._mutable = True
        if getattr(request.data, 'user', None) or getattr(request.data, 'post', None):
            raise exceptions.ValidationError(detail="Invalid body parameters: post/user cannot be specified")
        request.data['reaction'] = str(request.data['reaction'])
        request.data['post'] = reverse('api:post-detail', args=[kwargs['post_pk']])
        if not is_mutable:
            request.data._mutable = False
        return super().create(request, args, kwargs)