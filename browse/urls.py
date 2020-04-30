from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from browse import views

app_name = 'browse'

urlpatterns = [
	path('', views.Index.as_view(), name='home'),
	path('browse/', views.Index.as_view(), name='package-list'),
	path('offer/', views.Index, name='offer-list'),
	path('about/', views.Index),
	path('contact/', views.Index),
	path('branch_pkg_availability/', views.Index),
	path('browse/filter/', views.Index, name='rating_filter'),

	path('browse/restaurants/', views.Index.as_view(), name='restaurants'),
	path('browse/branches/', views.Index.as_view(), name='branches'),

	# path('menuEntryForRestaurant/', views.RestaurantMenuEntryList.as_view()),
	# path('branchListForRestaurant/', views.RestaurantBranchList.as_view())
	path('browse/raw/', views.Index),
	path('browse/upload/', views.AddMemeView.as_view()),

	path('browse/item/<int:id>/', views.Index.as_view(), name='package-details'),
	path('browse/item/<int:id>/submitReview/', views.Index),
	path('browse/item/<int:id>/submitRating/', views.Index),
	path('browse/item/<int:id>/reactOn/', views.Index),

	path('browse/restaurants/<int:id>/', views.Index.as_view(), name='restaurant_detail'),

	path('browse/branches/<int:id>/', views.Index.as_view(), name='Branch_detail'),
	path('browse/branches/<int:id>/submitRating/', views.Index),
	path('browse/branches/<int:id>/submitReview/', views.Index),
	path('browse/branches/<int:id>/reactOn/', views.Index),

	path('order/checkout/', views.Index.as_view(), name='checkout'),
	path('order/checkout/bkashPayment', views.Index, name='bkashPayment'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
