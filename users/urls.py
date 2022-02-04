from django.urls import include, path, register_converter
from .views import index_view, user_detail_view
# from .converters import StravaAuthTokenCodeConverter

# register_converter(StravaAuthTokenCodeConverter, 'exchangeToken')

urlpatterns = [
    # path('', index_view), # users - index
    # path('//<exchangeToken:code>', user_detail_view, name='detail'),
    ]
