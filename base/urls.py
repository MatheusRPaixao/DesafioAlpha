from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('search-stock', views.search_stock_view, name='search_stock'),
    path('update-stock-observer', views.update_stock_observer, name='update_stock_observer'),
]
