from django.urls import include, path
from rest_framework_nested import routers

import coreapp.views.PostViewSet
import coreapp.views.UserViewSet
import coreapp.views.PostReactionViewSet
import coreapp.views.PostModerationViewSet
import coreapp.views.CommentViewSet
import coreapp.views.PostCommentViewSet

router = routers.SimpleRouter()
router.register(r'post', coreapp.views.PostViewSet.PostViewSet, basename='post')
router.register(r'comment', coreapp.views.CommentViewSet.CommentViewSet, basename='comment')
router.register(r'moderation/post', coreapp.views.PostModerationViewSet.PostModerationViewSet,
                basename='moderation-post')

# router.register(r'keyword', views.KeywordViewSet, basename='keyword')
router.register(r'user', coreapp.views.UserViewSet.UserViewSet, basename='user')

post_router = routers.NestedSimpleRouter(router, r'post', lookup='post')
post_router.register(r'reaction', coreapp.views.PostReactionViewSet.PostReactionViewSet, basename='post-reaction')
post_router.register(r'comment', coreapp.views.PostCommentViewSet.PostCommentViewSet, basename='post-comment')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(post_router.urls)),
    # path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]
