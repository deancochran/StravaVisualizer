from django.http import request
from django.urls import path, re_path
from . import views

app_name = 'celery_progress'
urlpatterns = [
    # re_path(r'^(?P<task_id>[\w-]+)/$', views.get_progress, name='task_status'),
    re_path(r'^(?P<task_id>[\w-]+)/$', views.task_status, name='task_status')
]
