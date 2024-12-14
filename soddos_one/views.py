from django.http import HttpResponse
from django.shortcuts import render
from spost.models import Post


# Create your views here.
def index(request):
    posts = Post.objects.select_related('author').order_by('-create_dt')[:3]
    return render(request, 'index.html', context={'posts': posts})