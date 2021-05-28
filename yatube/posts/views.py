from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from yatube.settings import COUNT_OF_PAGES

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    page_number = request.GET.get('page')
    post_list = Post.objects.all()

    paginator = Paginator(post_list, COUNT_OF_PAGES)
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {
            'page': page,
        }
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    page_number = request.GET.get('page')
    post_list = Post.objects.all()
    paginator = Paginator(post_list, COUNT_OF_PAGES)
    page = paginator.get_page(page_number)
    return render(request,
                  'post/group.html',
                  {
                      'group': group,
                      'page': page
                  }
                  )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    paginator = Paginator(posts, COUNT_OF_PAGES)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'post/profile.html',
        {
            'author': author,
            'page': page,
        }
    )


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id, author__username=username)
    return render(request, 'post/post.html',
                  {'author': author,
                   'post': post})


@login_required()
def post_edit(request, username, post_id):
    is_edit = 1
    post = get_object_or_404(Post, id=post_id, author__username=username)
    if post.author != request.user:
        return redirect('post', username=username, post_id=post_id)
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('post', username=username, post_id=post_id)
    return render(request, 'post/new.html',
                  {
                      'form': form,
                      'post_id': post_id,
                      'is_edit': is_edit
                  }
                  )


@login_required
def new_post(request):
    is_edit = 0
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('index')
    return render(request, 'post/new.html',
                  {
                      'form': form,
                      'is_edit': is_edit,
                  }
                  )
