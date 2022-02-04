from django.http import request
from django.shortcuts import render
from users.models import User
# Create your views here.

def index_view(request):
    """
    This view displays all the users that have been made
    """
    user_objs = User.objects.all()
    context={
            'users':user_objs,
        }
    return render(request, 'users/users_index.html', context)
    

def user_detail_view(request, code, *args, **kwargs):
    print(code)
    context={
        'user':'user'
    }
    return render(request, 'users/user_detail.html')