from datetime import datetime
from django.db import models
from django.shortcuts import render, get_object_or_404
from .models import Post, Category, User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import PostForm
from django.shortcuts import render, get_object_or_404, redirect
from django import forms


def posts():
    """Получение постов из БД"""
    return Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.now()
    )


def index(request):
    posts = Post.objects.filter(is_published=True).order_by("-created_at")
    paginator = Paginator(posts, 10)  # 10 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/index.html", {"page_obj": page_obj})



def get_paginator(request, items, num=10):
    """Создает объект пагинации."""
    paginator = Paginator(items, num)
    num_pages = request.GET.get('page')
    return paginator.get_page(num_pages)

def post_detail(request, post_id):  # Используем post_id вместо id
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})


def category_posts(request, category_slug):
    """Отображение публикаций категории"""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    context = {'category': category,
               'post_list': posts().filter(category=category)}
    return render(request, 'blog/category.html', context)


def profile(request, username):
    """Возвращает профиль пользователя."""
    template = 'blog/profile.html'
    user = get_object_or_404(User, username=username)
    posts_list = (
        user.posts
        .order_by('-pub_date')
    )
    page_obj = get_paginator(request, posts_list)
    context = {'profile': user, 'page_obj': page_obj}
    return render(request, "blog/profile.html", {"profile_user": user})


@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Установка автора как текущего пользователя
            post.save()
            return redirect('blog:index')  # Перенаправление на главную страницу
    else:
        form = PostForm()
    return render(request, 'blog/add_post.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog:index")
    else:
        form = PostForm(instance=post)
    return render(request, "blog/edit_post.html", {"form": form, "post": post})



@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect("blog:index")
    return render(request, "blog/delete_post.html", {"post": post})


def about(request):
    return render(request, 'pages/about.html')  # Шаблон "О проекте"

def rules(request):
    return render(request, 'pages/rules.html')  # Шаблон "Наши правила"