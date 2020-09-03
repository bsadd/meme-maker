from rest_framework import mixins, viewsets

from coreapp.models import PostComment
from coreapp.pagination import StandardResultsSetPagination
from coreapp.serializers.PostCommentSerializers import PostCommentCreateSerializer


class PostCommentViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """
    API endpoint to list comments on an approved posts.
    """
    pagination_class = StandardResultsSetPagination
    serializer_class = PostCommentCreateSerializer

    def get_queryset(self):
        qs = PostComment.objects.all().of_approved_posts()
        if 'post_pk' in self.kwargs:
            qs = qs.of_post(self.kwargs['post_pk'])
        return qs