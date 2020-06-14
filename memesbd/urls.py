from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from memesbd import views, views_json

app_name = 'memesbd'

urlpatterns = [
    path('', views.view_meme_gallery, name='home'),
    path('memesbd/', views.Index.as_view(), name='post-list'),

    path('memesbd/raw/', views.Index),
    path('memesbd/upload/', views.AddMemeView.as_view(), name='upload-page'),

    path('memesbd/upload-image-template/', views.upload_meme_image, name='upload-template-image'),
    path('memesbd/upload-image-edited/', views.upload_meme_image, name='upload-meme-image'),

    path('memesbd/item/<int:id>/', views.memeDetails, name='view-meme'),
    path('memesbd/item/<int:id>/edit/', views.editView, name='edit-meme'),

    path('memesbd/item/<int:id>/submitReview/', views.Index, name='comment-meme'),
    path('memesbd/item/<int:id>/reactOn/', views.update_react, name='rate-meme'),

    path('profile/posts/', views.approved_posts, name='approved-posts'),
    path('profile/pending-posts/', views.pending_posts, name='pending-posts'),

    path('moderation/pending-posts/', views.pending_posts_moderator, name='pending-posts-moderator'),

    path('moderation/pending-posts/<int:id>/approve', views.approve_post_moderator, name='approve-post'),
    path('moderation/pending-posts/<int:id>/delete', views.delete_post_moderator, name='delete-post'),

    path('hapi/meme/list', views_json.meme_list, name='hapi-meme-list'),
    path('hapi/meme/create', views_json.meme_create, name='hapi-meme-create'),
    path('hapi/moderation/action', views_json.moderation_action, name='hapi-moderate-action'),
    path('hapi/reaction/submit', views_json.react_submit, name='hapi-react-submit'),
    path('hapi/comment/submit', views_json.comment_submit, name='hapi-comment-submit'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
