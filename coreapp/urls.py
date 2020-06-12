from django.urls import include, path
from rest_framework import routers

from coreapp import views

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'keywords', views.KeywordViewSet, basename='keyword')
router.register(r'users', views.UserViewSet, basename='user')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    # path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]
