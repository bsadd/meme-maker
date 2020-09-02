from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from filters.mixins import FiltersMixin
from rest_framework import status, viewsets, filters, exceptions
from rest_framework.decorators import action

from coreapp.filters import PostCategoryFilter, PostSearchFilter
from coreapp.models import Post
from coreapp.pagination import StandardResultsSetPagination
from coreapp.permissions import IsAuthenticatedCreateOrOwnerModifyOrReadOnly
from coreapp.serializers.PostSerializers import PostSerializer, PostModerationSerializer
from coreapp.swagger import query_params
from coreapp.utils import to_bool
from coreapp.validators import post_query_schema


@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(operation_summary='Details of a post',
                                                responses={status.HTTP_404_NOT_FOUND: 'Post not found/approved'}))
@method_decorator(name='list',
                  decorator=swagger_auto_schema(operation_summary='List of posts',
                                                manual_parameters=query_params.POST_LIST_QUERY_PARAMS))
@method_decorator(name='create',
                  decorator=swagger_auto_schema(operation_summary='Uploads a new post',
                                                manual_parameters=[query_params.REQUIRED_AUTHORIZATION_PARAMETER]))
@method_decorator(name='update',
                  decorator=swagger_auto_schema(operation_summary='Modifies a post',
                                                manual_parameters=[query_params.REQUIRED_AUTHORIZATION_PARAMETER],
                                                responses={status.HTTP_404_NOT_FOUND: 'Post not found'}))
class PostViewSet(FiltersMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows Post to be created/viewed/edited.
    TODO: validation using models
    TODO: check timezone
    TODO: uploader=me
    """
    filter_backends = (PostCategoryFilter, PostSearchFilter, filters.OrderingFilter)
    filter_mappings = {
        'uploader': 'user_id__in',
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

    permission_classes = (IsAuthenticatedCreateOrOwnerModifyOrReadOnly,)
    http_method_names = ['get', 'post', 'put']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Post.objects.all().first()
        if self.action == 'related':
            return Post.objects.get_related_posts(post_id=self.kwargs.get('pk', None)).prefetch_related('reactions',
                                                                                                        'user')
        return Post.objects.prefetch_related('reactions', 'user').all()

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)

    @swagger_auto_schema(method='get',
                         operation_summary='List of related posts',
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