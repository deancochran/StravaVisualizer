
import base64
import imp
import io
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
# from activities.models import set_activities
from users.models import User
from users.tasks import  load_elevations
from celery import group

@login_required
def user_detail_view(request, *args, **kwargs):
    username = request.user.username
    user = User.objects.filter(username = username)
    if len(user) > 1:
        print('there are duplicate instances of this username.. issue unsolved')
        # username = get_new_username()
        # user = User.objects.get(username = username)
    else:
        user = User.objects.get(username = username)
        if user.expires_at != None:
            print('checking user access')
            user.update_access()
            print('checking user activities')
            if user.has_activities():
                print('downloading new activities')
                user.download_activities(only_new_activities=True)
                activity_ids = [x.id for x in user.get_activities(missing_elevations=True)]
                result = load_elevations.delay(activity_ids)

                print('result.task_id',result.task_id)
                return render(request,'users/user_detail.html',context={
                    'user':user,
                    'task_id': result.task_id
                })
            else:
                print('downloading all activities')
                user.download_activities(only_new_activities=False)

   
                activity_ids = [x.id for x in user.get_activities(missing_elevations=True)]
                result = load_elevations.delay(activity_ids)
                return render(request,'users/user_detail.html',context={
                    'user':user,
                    'task_id': result.task_id
                })
        else:
            if user.has_access(request):
                if user.has_activities():
                    user.download_activities(only_new_activities=True)

                    activity_ids = [x.id for x in user.get_activities(missing_elevations=True)]
                    result = load_elevations.delay(activity_ids)
                    return render(request,'users/user_detail.html',context={
                    'user':user,
                    'task_id': result.task_id
                })
                else:
                    user.download_activities()

                    activity_ids = [x.id for x in user.get_activities(missing_elevations=True)]
                    result = load_elevations.delay(activity_ids)
                    return render(request,'users/user_detail.html',context={
                    'user':user,
                    'task_id': result.task_id
                })
            else:
                print(user['access_token'])
                print('undevloped outcome.. ask user to login in and authenticate again')

@login_required
def get_landscapes_view(request, *args, **kwargs):
    print('made it to the landscapes view')
    username = request.user.username
    user = User.objects.get(username = username)
    img = user.get_landscapes_img()
    response = HttpResponse(content_type='image/png')
    img.save(response, "PNG") 
    return response

@login_required
def get_routes_view(request, *args, **kwargs):
    print('made it to the routes view')
    username = request.user.username
    user = User.objects.get(username = username)
    img = user.get_routes_img()
    response = HttpResponse(content_type='image/png')
    img.save(response, "PNG") 
    return response