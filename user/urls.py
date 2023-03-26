from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('sign-up/', views.create_user_view, name='sign_up'),
    path('logout/', views.logout_view, name='logout'),
]