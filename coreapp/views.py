from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import exceptions

from coreapp.decorators import *
from coreapp.permissions import IsModerator
from memesbd import utils_db
from memesbd.models import *
from memesbd.serializers import *


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    TODO: validation using models
    TODO: enforce author edit only
    """
    search_fields = ['caption', 'author__username', 'keywordlist__keyword__name']
    filter_backends = (filters.SearchFilter,)

    serializer_class = PostSerializer  # default serializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    http_method_names = ['get', 'post']

    queryset = Post.approved.order_by('id')

    @action(detail=True, methods=['POST'], permission_classes=[IsModerator],
            url_path='approval', url_name='approval')
    def approval(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            approval_status = str(request.data['approval_status']).upper()
            if approval_status not in ['APPROVE', 'REJECT']:
                raise exceptions.ValidationError(detail="Invalid 'approval_status'")
            elif post.approval_status == ApprovalStatus.APPROVED and approval_status == 'APPROVE':
                raise exceptions.NotAcceptable(detail="Already approved")
            elif post.approval_status == ApprovalStatus.REJECTED and approval_status == 'REJECT':
                raise exceptions.NotAcceptable(detail="Already rejected")
            else:
                post.approval_status = ApprovalStatus.APPROVED if approval_status == 'APPROVE' else ApprovalStatus.REJECTED
                post.moderator = request.user
                post.approval_at = timezone.now()
                post.save()
                return Response(PostSerializer(post, context={'request': request}).data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            raise exceptions.NotFound
        except KeyError:
            raise exceptions.NotAcceptable(detail="'approval_status' field must be provided")

    @action(detail=True, methods=['GET'],
            url_path='related', url_name='related-posts')
    def related(self, request, pk):
        try:
            posts = utils_db.get_related_posts(post_id=pk)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            raise exceptions.NotFound

    @action(detail=False, methods=['GET'], permission_classes=[IsModerator],
            url_path='pending', url_name='pending-posts')
    def pending(self, request):
        posts = Post.objects.filter(approval_status=ApprovalStatus.PENDING)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated],
            url_path='my-posts', url_name='my-posts')
    def my_posts(self, request):
        posts = Post.objects.filter(author=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class KeywordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows keywords to be viewed or created but not to be modified.
    """
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    http_method_names = ['get', 'post']


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put']

    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated],
            url_path='current', url_name='current')
    def current_user(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)


class PostReactViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # queryset = PostReact.objects.filter(post__approval_status=ApprovalStatus.APPROVED)
    serializer_class = PostReactSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    http_method_names = ['get', 'post']

    # lookup_field = 'post__id'

    def get_queryset(self):
        return PostReact.objects.filter(post_id=self.kwargs['post_pk'], post__approval_status=ApprovalStatus.APPROVED)

    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated],
            url_path='user', url_name='user')
    def user(self, request, post_pk=None):
        """post/1/react/user
        current user's react only
        """
        try:
            '''
            TODO: should check post existence?
            '''
            post = Post.objects.get(id=post_pk, approval_status=ApprovalStatus.APPROVED)
            return Response(PostReactSerializer(PostReact.objects.get(post=post, user=request.user)).data,
                            status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            raise exceptions.NotFound(detail="No such react-able post exists with this id")
        except PostReact.DoesNotExist:
            raise exceptions.NotFound(detail="No react on the post from this user")

    def create(self, request, *args, **kwargs):
        request.data['react'] = str(request.data['react']).upper()
        request.data['post'] = kwargs['post_pk']
        return super().create(request, args, kwargs)
