import json
from django.http import HttpResponse
from celery.result import AsyncResult
from celery_progress.backend import Progress
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


@never_cache
def get_progress(request, task_id):
    progress = Progress(AsyncResult(task_id))
    return HttpResponse(json.dumps(progress.get_info()), content_type='application/json')

@login_required
def task_status(request, task_id):
    # Other checks could go here
    return get_progress(request, task_id)