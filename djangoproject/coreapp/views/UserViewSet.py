from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSerializer
from coreapp.pagination import StandardResultsSetPagination
from coreapp.swagger import query_params


@method_decorator(name='list',
                  decorator=swagger_auto_schema(operation_summary="List of users"))
@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(operation_summary="Details of a user"))
class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(operation_summary="Current user Profile",
                         manual_parameters=[query_params.REQUIRED_AUTHORIZATION_PARAMETER],
                         responses={status.HTTP_401_UNAUTHORIZED: 'User is not authenticated'})
    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated],
            url_path='current', url_name='current')
    def current_user(self, request):
        return Response(UserSerializer(request.user, context={'request': request}).data, status=status.HTTP_200_OK)