from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from . import forms
from .models import Post


def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    context = {
        "posts": posts
    }
    return render(request, 'posts/posts_list.html', context)

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    context = {
        "post": post
    }
    return render(request, 'posts/post_page.html', context)

@login_required(login_url='/users/login/')
def post_new(request):
    if request.method == 'POST': 
        form = forms.CreatePost(request.POST, request.FILES) 
        if form.is_valid():
            newpost = form.save(commit=False) 
            newpost.author = request.user 
            newpost.save()
            return redirect('posts:list')
    else:
        form = forms.CreatePost()
    return render(request, 'posts/post_new.html', { 'form': form })