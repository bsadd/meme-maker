from django.urls import include, path
from rest_framework_nested import routers

from coreapp import views

router = routers.SimpleRouter()
router.register(r'post', views.PostViewSet, basename='post')
router.register(r'moderation/post', views.PostModerationViewSet, basename='moderation-post')

# router.register(r'keyword', views.KeywordViewSet, basename='keyword')
router.register(r'user', views.UserViewSet, basename='user')

post_router = routers.NestedSimpleRouter(router, r'post', lookup='post')
post_router.register(r'react', views.PostReactViewSet, basename='post-react')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(post_router.urls)),
    # path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]
