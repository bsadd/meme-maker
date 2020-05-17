from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from memesbd import views

app_name = 'memesbd'

urlpatterns = [
    path('', views.view_meme_gallery, name='home'),
    path('memesbd/', views.Index.as_view(), name='post-list'),

    path('memesbd/raw/', views.Index),
    path('memesbd/upload/', views.AddMemeView.as_view(), name='upload-page'),

    path('memesbd/upload-image-template/', views.upload_meme_image, name='upload-template-image'),
    path('memesbd/upload-image-edited/', views.upload_meme_image, name='upload-meme-image'),
    # path('memesbd/edit/', views.contactSection, name='image-edit'),

    path('memesbd/item/<int:id>/', views.memeDetails, name='view-meme'),
    path('memesbd/item/<int:id>/edit/', views.editView, name='edit-meme'),

    path('memesbd/item/<int:id>/submitReview/', views.Index, name='comment-meme'),
    path('memesbd/item/<int:id>/submitRating/', views.Index, name='rate-meme'),
    path('memesbd/item/<int:id>/reactOn/', views.Index, name='react-comment'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
