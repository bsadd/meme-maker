from django.contrib.auth.decorators import user_passes_test
from django.urls import path, include

from accounts import views

app_name = 'accounts'

login_forbidden = user_passes_test(lambda u: u.is_anonymous, '/', redirect_field_name=None)

urlpatterns = [
    # path('login/', views.LoginView.as_view(), name='login'),
    path('login/', login_forbidden(views.SignupLoginView.as_view()), name='login'),

    path('admin-login/', views.LoginView.as_view(), name='admin-login'),

    path('register/', views.SignupLoginView.as_view(), name='register'),
    path(r'register/facebook-signUp/', include('allauth.urls'), name='facebook-signUp'),

    path('recovery/', views.LoginView, name='recovery'),

    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('admin-logout/', views.LoginView.as_view(), name='admin-logout'),

]
