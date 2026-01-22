from django.shortcuts import render, redirect
from .models import Post, Follow, Comment
from django.contrib.auth.models import User

from . import forms
from .forms_register import RegisterForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django import forms as django_forms

# Create your views here.
@login_required(login_url='blog:login')
def homepage(request):
    following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    posts = Post.objects.filter(author__in=following_ids)
    return render(request, 'photos/post_lists.html', {'posts': posts})
def about(request):
    return render(request,"photos/about.html")
def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    comments = post.comments.select_related('author').order_by('-created')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:page', slug=slug)
    else:
        form = CommentForm()
    return render(request, 'photos/post_page.html', {'post': post, 'comments': comments, 'form': form})
@login_required(login_url='blog:login')
def post_new(request):
    if request.method == 'POST': 
        form = forms.CreatePost(request.POST, request.FILES) 
        if form.is_valid():
            newpost = form.save(commit=False) 
            newpost.author = request.user 
            newpost.save()
            return redirect('blog:home')
    else:
        form = forms.CreatePost()
    return render(request, 'photos/post_new.html', { 'form': form })
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:home')
    else:
        form = RegisterForm()
    return render(request, 'photos/register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('blog:home')
    else:
        form = AuthenticationForm()
    return render(request, 'photos/login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('blog:home')
@login_required(login_url='blog:login')
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'photos/my_posts.html', {'posts': posts})

@login_required(login_url='blog:login')
def edit_post(request, slug):
    post = Post.objects.get(slug=slug, author=request.user)
    if request.method == 'POST':
        form = forms.CreatePost(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:my-posts')
    else:
        form = forms.CreatePost(instance=post)
    return render(request, 'photos/edit_post.html', {'form': form, 'post': post})

@login_required(login_url='blog:login')
def delete_post(request, slug):
    post = Post.objects.get(slug=slug, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:my-posts')
    return render(request, 'photos/delete_post.html', {'post': post})

@login_required(login_url='blog:login')
def follow_user(request, user_id):
    user_to_follow = User.objects.get(id=user_id)
    if user_to_follow != request.user:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('blog:user-list')

@login_required(login_url='blog:login')
def unfollow_user(request, user_id):
    user_to_unfollow = User.objects.get(id=user_id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('blog:user-list')

@login_required(login_url='blog:login')
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    following_ids = set(Follow.objects.filter(follower=request.user).values_list('following_id', flat=True))
    return render(request, 'photos/user_list.html', {'users': users, 'following_ids': following_ids})

class CommentForm(django_forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']