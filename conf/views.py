from django.shortcuts import render
# from blog.models import Post

def index_view(request):
    """
    The home function takes a request and returns an HTML string to display to the index page of our site
    """
    return render(request, 'index.html')
    