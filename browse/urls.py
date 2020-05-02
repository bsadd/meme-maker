from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from browse import views

app_name = 'browse'

urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('browse/', views.Index.as_view(), name='package-list'),

    path('browse/raw/', views.Index),
    path('browse/upload/', views.AddMemeView.as_view(), name='upload-page'),

    path('browse/upload-image-template/', views.upload_meme_image, name='upload-template-image'),
    path('browse/upload-image-edited/', views.upload_meme_image, name='upload-meme-image'),
    # path('browse/edit/', views.contactSection, name='image-edit'),

    path('browse/item/<int:id>/', views.editView, name='view-meme'),
    path('browse/item/<int:id>/edit/', views.editView, name='edit-meme'),

    path('browse/item/<int:id>/submitReview/', views.Index, name='comment-meme'),
    path('browse/item/<int:id>/submitRating/', views.Index, name='rate-meme'),
    path('browse/item/<int:id>/reactOn/', views.Index, name='react-comment'),

    path('browse/test/', views.editView, name='rating_filter'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
