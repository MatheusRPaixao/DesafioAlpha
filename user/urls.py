from django.urls import path
from . import views

urlpatterns = [
    path('user-login/', views.login_view, name='user_login'),
    path('sign-up/', views.create_user_view, name='sign_up'),
    path('user-logout/', views.logout_view, name='user_logout'),
]
