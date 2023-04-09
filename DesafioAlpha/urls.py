from django.contrib import admin
from django.urls import path, include

from user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('base.urls')),

    path('', include('django.contrib.auth.urls')),
    path('', include('user.urls')),

    path('accounts/login', user_views.login_view),
]
