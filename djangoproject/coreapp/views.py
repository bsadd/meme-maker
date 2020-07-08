from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from filters.mixins import FiltersMixin
from rest_framework import viewsets, status, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from coreapp.pagination import StandardResultsSetPagination
from coreapp.permissions import IsModerator
from coreapp.filters import *
from coreapp.serializers import *
from coreapp.swagger import query_params
from coreapp.swagger.schema import PostReactCreateSchema
from coreapp.swagger.serializers import PostReactRequestBodySerializer, PostReactResponseBodySerializer
from coreapp.utils import to_bool
from coreapp.validators import post_query_schema


@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(responses={status.HTTP_404_NOT_FOUND: 'Post not found/approved'}))
@method_decorator(name='list',
                  decorator=swagger_auto_schema(manual_parameters=query_params.POST_LIST_QUERY_PARAMS))
@method_decorator(name='create',
                  decorator=swagger_auto_schema(manual_parameters=[query_params.REQUIRED_AUTHORIZATION_PARAMETER]))
@method_decorator(name='update',
                  decorator=swagger_auto_schema(manual_parameters=[query_params.REQUIRED_AUTHORIZATION_PARAMETER],
                                                responses={status.HTTP_404_NOT_FOUND: 'Post not found'}))
class PostViewSet(FiltersMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows Post to be created/viewed/edited.
    TODO: validation using models
    TODO: enforce author edit only
    TODO: check timezone
    TODO: uploader=me
    """
    filter_backends = (PostCategoryFilter, PostSearchFilter, filters.OrderingFilter)
    filter_mappings = {
        'uploader': 'author_id__in',
        'violent': 'is_violent',
        'adult': 'is_adult',
        'keyword': 'keywordlist__keyword__name__in',
        'uploaded-before': 'uploaded_at__lt',
        'uploaded-after': 'uploaded_at__gte',
        'uploaded-on': 'uploaded_at__date',
        'template': 'template__isnull',
    }
    filter_value_transformations = {
        'violent': lambda val: to_bool(val),
        'adult': lambda val: to_bool(val),
        'template': lambda val: to_bool(val),
        'keyword': lambda val: filter(None, val.strip().lower().split(',')),
    }
    filter_validation_schema = post_query_schema
    search_fields = ['caption', 'author__username', 'keywordlist__keyword__name']
    search_fields_mappings = {'caption': 'caption',
                              'uploader': 'author__username',
                              'keyword': 'keywordlist__keyword__name'}
    search_param = 'q'
    ordering_fields = ['uploaded_at', 'nviews']
    ordering = ['-uploaded_at']

    pagination_class = StandardResultsSetPagination
    serializer_class = PostSerializer
    serializer_classes = {
        'pending': PostModerationSerializer,
    }

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    http_method_names = ['get', 'post', 'put']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Post.objects.all()
        if self.action == 'related':
            return Post.objects.get_related_posts(post_id=self.kwargs.get('pk', None)).prefetch_related('reacts',
                                                                                                        'author')
        return Post.objects.prefetch_related('reacts', 'author').all()

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)

    @swagger_auto_schema(method='get',
                         operation_description="Returns list of posts made on the same template of post=pk",
                         responses={status.HTTP_404_NOT_FOUND: 'No such post exists with provided pk'},
                         manual_parameters=query_params.POST_LIST_QUERY_PARAMS)
    @action(detail=True, methods=['GET'],
            url_path='related', url_name='related-posts')
    def related(self, request, pk):
        try:
            return super().list(request, pk=pk)
        except Post.DoesNotExist:
            raise exceptions.NotFound(detail='No such post exists with id=%s' % pk)


class KeywordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows keywords to be viewed or created but not to be modified.
    """
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    http_method_names = ['get', 'post']


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(operation_description="Returns current user profile's detail",
                         responses={status.HTTP_401_UNAUTHORIZED: 'User is not authenticated'})
    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated],
            url_path='current', url_name='current')
    def current_user(self, request):
        return Response(UserSerializer(request.user, context={'request': request}).data, status=status.HTTP_200_OK)


@method_decorator(name='list',
                  decorator=swagger_auto_schema(responses={status.HTTP_404_NOT_FOUND: 'Post not found/approved'}))
class PostReactViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """
    API endpoint that allows users to react or view reactions on approved posts.
    """
    serializer_class = PostReactSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        qs = PostReact.objects.all().of_approved_posts()
        if 'post_pk' in self.kwargs:
            qs = qs.of_post(self.kwargs['post_pk'])
        return qs

    @swagger_auto_schema(method='get', operation_description="Returns current user's reaction on the post",
                         responses={status.HTTP_404_NOT_FOUND: 'Post/Reaction Not found'})
    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated],
            url_path='user', url_name='user')
    def user(self, request, post_pk=None):
        """
        currently authenticated user's react only
        """
        try:
            post = Post.objects.get(id=post_pk, approval_status=ApprovalStatus.APPROVED)
            return Response(PostReactSerializer(PostReact.objects.get(post=post, user=request.user),
                                                context={'request': request}).data,
                            status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            raise exceptions.NotFound(detail="No such react-able post exists with this id")
        except PostReact.DoesNotExist:
            raise exceptions.NotFound(detail="No react on the post from this user")

    @swagger_auto_schema(request_body=PostReactRequestBodySerializer,
                         operation_description="Create/Change/Remove current user's reaction on the post",
                         manual_parameters=[query_params.REQUIRED_AUTHORIZATION_PARAMETER],
                         responses={status.HTTP_201_CREATED: PostReactResponseBodySerializer,
                                    status.HTTP_401_UNAUTHORIZED: 'User not authorized',
                                    status.HTTP_400_BAD_REQUEST: 'post/user passed in request body',
                                    status.HTTP_404_NOT_FOUND: 'Post Not found'})
    def create(self, request, *args, **kwargs):
        is_mutable = True if getattr(request.data, '_mutable', True) else request.data._mutable
        if not is_mutable:
            request.data._mutable = True
        if getattr(request.data, 'user', None) or getattr(request.data, 'post', None):
            raise exceptions.ValidationError(detail="Invalid body parameters: post/user cannot be specified")
        request.data['react'] = str(request.data['react'])
        request.data['post'] = reverse('api:post-detail', args=[kwargs['post_pk']])
        if not is_mutable:
            request.data._mutable = False
        return super().create(request, args, kwargs)


class PostModerationViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    """
    API endpoint to allow moderators to approve/moderate posts
    """
    pagination_class = StandardResultsSetPagination
    serializer_class = PostModerationSerializer
    permission_classes = (IsModerator,)
    queryset = Post.objects.prefetch_related('reacts', 'author').all()
