from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import exceptions

from coreapp.decorators import *
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
    search_fields = ['caption', 'author__username']  # , 'author'
    filter_backends = (filters.SearchFilter,)
    serializer_classes = {
        'react': PostReactSerializer,
    }
    default_serializer_class = PostSerializer  # default serializer
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    queryset = Post.objects.filter(approval_status=ApprovalStatus.APPROVED).order_by('id')

    # serializer_class = PostSerializer

    @action(detail=True, methods=['GET', 'POST', 'PUT', 'DELETE'])
    @method_decorator(api_auth_required)
    def react(self, request, pk):
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
            return Response(PostReactSerializer(post_react).data, status=status.HTTP_202_ACCEPTED)
        except Post.DoesNotExist:
            raise exceptions.NotFound(detail="No such post exists with this id")
        except PostReact.DoesNotExist:
            raise exceptions.NotFound(detail="No react on the post from this user")
        except (ValidationError, KeyError):
            raise exceptions.ValidationError

    @action(detail=True, methods=['POST'])
    @method_decorator(moderator_login_required)
    def approve(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            # if 'set' not in request.GET:
            #     raise exceptions.NotAcceptable(detail="'set' field not submitted")
            # is_approved = bool(request.GET['set'])
            # print(is_approved)
            if post.approval_status == ApprovalStatus.APPROVED:
                raise exceptions.NotAcceptable(detail="Already approved")
            post.approval_status = ApprovalStatus.APPROVED
            post.moderator = request.user
            post.save()
            return Response(PostSerializer(post).data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            raise exceptions.NotFound

    @action(detail=True, methods=['POST'])
    @method_decorator(moderator_login_required)
    def reject(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            if post.approval_status == ApprovalStatus.APPROVED:
                raise exceptions.NotAcceptable(detail="Already rejected")
            post.approval_status = ApprovalStatus.REJECTED
            post.moderator = request.user
            post.save()
            return Response(PostSerializer(post).data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            raise exceptions.NotFound


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
