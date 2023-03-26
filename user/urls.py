from django.urls import path
from . import views

urlpatterns = [
    path('login-user/', views.login_view, name='login_user'),
    path('create_user/', views.create_user_view, name='create_user'),
]