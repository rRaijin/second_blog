from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.template.context_processors import csrf
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect, render_to_response

from blog import models
from .forms import PostForm, CommentForm
from .models import Post, PostCategory, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def category(request, category_name):
    category_list = PostCategory.objects.all()
    category = PostCategory.objects.get(category_name=category_name)
    queryset_list = Post.objects.filter(category=category)
    paginator = Paginator(queryset_list, 4)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        'category': category,
        'post': queryset,
        "page_request_var": page_request_var,
        "category_list": category_list
    }
    return render(request, 'blog/category.html', context)

def post_create(request, category_name):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "Пока только модераторы могут добавлять статью. Позже это будет исправлено.")
        return redirect('/')
    # if not request.user.is_staff and not request.user.is_superuser:
    #     raise Http404
    cat = get_object_or_404(PostCategory, category_name=category_name)
    form = PostForm(request.POST or None, request.FILES or None)
    poster = request.user
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = poster
        instance.category = cat
        instance.save()
        messages.success(request, "Пост создан")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form
    }
    return render(request, "blog/post_form.html", context)

def add_comment(request, slug=None):
    if request.user.is_authenticated():
    # if request.POST and ("pause" not in request.session):
        form = CommentForm(request.POST or None)
        commentator = request.user
        if form.is_valid():
            comments = form.save(commit=False)
            comments.post = Post.objects.get(slug=slug)
            comments.commentator = commentator
            comments.save()
            # request.session.set_expiry(60)
            # request.session['pause'] = True
            messages.success(request, "Комментарий добавлен!")
    else:
        # messages.error(request, "Комментировать могут только зарегистрированные пользователи")
        return redirect('/auth/register/')
    return redirect('posts:detail', slug=slug)

def post_detail(request, slug=None):
    category_list = PostCategory.objects.all()
    comment_form = CommentForm(request.POST or None, request.FILES or None)
    instance = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post__slug=slug)
    if slug in request.COOKIES:
        redirect('posts:detail', slug=slug)
    else:
        instance.views += 1
        instance.save()
        response = redirect('posts:detail', slug=slug)
        response.set_cookie(slug, "cookies_file")
        return response
    context = {
        "title": "detail",
        "instance": instance,
        "comments": comments,
        "form": comment_form,
        "category_list": category_list,
    }
    return render(request, 'blog/post_detail.html', context)

def post_list(request):
    category_list = PostCategory.objects.all()
    queryset_list = Post.objects.all()
    popular = Post.objects.all().order_by("-views")[:4]
    latest = Post.objects.all().order_by("-created_date")[:4]
    paginator = Paginator(queryset_list, 5)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        "object_list": queryset,
        "category_list":category_list,
        "title": "Статьи",
        "page_request_var":page_request_var,
        "popular": popular,
        "latest": latest,
    }
    return render(request, 'blog/main.html', context)

def post_update(request, slug=None):
    if not request.user.is_superuser:
        raise Http404
    # if not request.user.is_staff and not request.user.is_superuser:
    #     raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    poster = request.user
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = poster
        instance.save()
        messages.success(request, "<a href='#'>item</a> Пост отредактирован", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title":instance.title,
        "instance":instance,
        "form": form,
    }
    return render(request, 'blog/post_form.html', context)

def post_delete(request, slug=None):
    if not request.user.is_superuser:
        raise Http404
    # if not request.user.is_staff and not request.user.is_superuser:
    #     raise Http404
    poster = request.user
    instance = get_object_or_404(Post, slug=slug)
    instance.author = poster
    instance.delete()
    messages.success(request, "<a href='#'>item</a> Пост удален", extra_tags='html_safe')
    return redirect("posts:list")

def add_likes(request, slug=None):
    if request.user.is_authenticated():
        if request.method == 'POST':
            post = Post.objects.get(slug=slug)
            user_tags = post.likedone.all()
            current_user = request.user
            if current_user not in user_tags:
                try:
                    post = get_object_or_404(Post, slug=slug)
                    post.likes += 1
                    post.likedone.add(current_user)
                    post.save()
                    data = {
                        'likes': post.likes,
                    }
                except ObjectDoesNotExist:
                    raise Http404
                return JsonResponse(data)
            return redirect('posts:detail', slug=slug)
    return redirect('posts:detail', slug=slug)

def add_dislike(request, slug=None):
    if request.user.is_authenticated():
        if request.method == 'POST':
            post = Post.objects.get(slug=slug)
            user_tags = post.likedone.all()
            current_user = request.user
            if current_user not in user_tags:
                try:
                    post = get_object_or_404(Post, slug=slug)
                    post.dislikes += 1
                    post.likedone.add(current_user)
                    post.save()
                    data = {
                        'dislikes': post.dislikes,
                    }
                except ObjectDoesNotExist:
                    raise Http404
                return JsonResponse(data)
            return redirect('posts:detail', slug=slug)
    return redirect('posts:detail', slug=slug)

