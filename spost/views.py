from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post
# Create your views here.

def post(request, id=None):
    if id != None:
        post = get_object_or_404(Post.objects.select_related('author'), id=id)
        print('Один пост ', post)
        return render(request, 'spost/posts.html', context={'post': post})
    else:
        posts = Post.objects.select_related('author').order_by('create_dt')[:5][::-1]
        print('Много постов ', posts)
        return render(request, 'spost/posts.html', context={'posts': posts})

@login_required  # Перенос проверки авторизации в декоратор
def create_post(request):
    form = PostForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/spost/post/')
    else:
        form = PostForm()
    return render(request, 'spost/create_post.html', context={'form': form})