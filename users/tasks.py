from __future__ import absolute_import
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from activities.models import set_elevation

@shared_task(bind=True)
def load_elevations(self, activity_ids):
    print(len(activity_ids),' are in need of elevation data')
    progress_recorder = ProgressRecorder(self)
    print('started progress recorder')
    result = 0
    i = 0
    for id in activity_ids:
        print('setting elevation for', id)
        set_elevation(id)
        result += i
        progress_recorder.set_progress(i + 1, len(activity_ids))
        i+=1
    return result