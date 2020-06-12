from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
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
    """
    search_fields = ['caption', 'author__username', 'keywordlist__keyword__name']
    filter_backends = (filters.SearchFilter,)
    serializer_classes = {
        'react': PostReactSerializer,
    }
    default_serializer_class = PostSerializer  # default serializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = Post.approved.order_by('id')

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    @action(detail=True, methods=['GET', 'POST', 'PUT', 'DELETE'], permission_classes=[permissions.IsAuthenticated],
            url_path='react', url_name='react')
    def react(self, request, pk):
        """post/1/react"""
        try:
            react = Reacts.NONE
            if request.method == 'GET':
                return Response(
                    PostReactSerializer(PostReact.objects.get(post=Post.objects.get(id=pk), user=request.user)).data,
                    status=status.HTTP_200_OK)
            if request.method != 'DELETE':
                react_name = str(request.data['react'])
                if react_name is None or react_name == '':
                    raise exceptions.ValidationError(detail="Not a valid react")
                react = Reacts.REACT_VALUE[react_name.upper()]
            from memesbd.utils_db import update_react_post
            post_react = update_react_post(user=request.user, post_id=pk, react=react)
            return Response(PostReactSerializer(post_react).data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            raise exceptions.NotFound(detail="No such post exists with this id")
        except PostReact.DoesNotExist:
            raise exceptions.NotFound(detail="No react on the post from this user")
        except (ValidationError, KeyError):
            raise exceptions.ValidationError

    @action(detail=True, methods=['POST'], permission_classes=[IsModerator],
            url_path='approval', url_name='approval')
    def approval(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            approval_status = str(request.data['approval_status']).lower()
            if approval_status not in ['approve', 'reject']:
                raise exceptions.ValidationError(detail="Invalid 'approval_status'")
            elif post.approval_status == ApprovalStatus.APPROVED and approval_status == 'approve':
                raise exceptions.NotAcceptable(detail="Already approved")
            elif post.approval_status == ApprovalStatus.REJECTED and approval_status == 'reject':
                raise exceptions.NotAcceptable(detail="Already rejected")
            else:
                post.approval_status = ApprovalStatus.APPROVED if approval_status == 'approve' else ApprovalStatus.REJECTED
                post.moderator = request.user
                post.approval_at = timezone.now()
                post.save()
                return Response(PostSerializer(post).data, status=status.HTTP_200_OK)
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
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated],
            url_path='current', url_name='current')
    def current_user(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
