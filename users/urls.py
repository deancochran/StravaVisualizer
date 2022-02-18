from unicodedata import name
from django.urls import include, path, re_path, register_converter
from .views import get_landscapes_view, get_routes_view, user_detail_view
# from .converters import StravaAuthTokenCodeConverter

app_name = 'users'
urlpatterns = [
    path('<str:username>/', user_detail_view, name='detail'),
    path('<str:username>/landsapes/', get_landscapes_view, name='landscapes'),
    path('<str:username>/routes/', get_routes_view, name='routes'),
    ]
