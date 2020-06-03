from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import exceptions

from coreapp.decorators import api_auth_required, route_permissions
from memesbd.models import *
from memesbd.serializers import *


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Post.objects.filter(approval_status=ApprovalStatus.APPROVED)
    serializer_class = PostSerializer

    @action(detail=True, methods=['POST'])
    @method_decorator(api_auth_required)
    def react(self, request, pk):
        try:
            react = str(request.data['react'])
            if react is None or react == '':
                raise exceptions.ValidationError
            react = react.upper()
            from memesbd.utils_db import update_react_post
            post_react = update_react_post(user=request.user, post_id=pk, react=Reacts.REACT_VALUE[react])
            return Response(PostReactSerializer(post_react).data, status=status.HTTP_202_ACCEPTED)
        except Post.DoesNotExist:
            raise exceptions.NotFound
        except (ValidationError, KeyError):
            raise exceptions.ValidationError


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
