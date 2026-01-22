from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('about/', views.about, name='about'),
    path('<slug:slug>',views.post_page, name="page"),
    path('new-post/', views.post_new, name="new-post"),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-posts/', views.my_posts, name='my-posts'),
    path('edit-post/<slug:slug>/', views.edit_post, name='edit-post'),
    path('delete-post/<slug:slug>/', views.delete_post, name='delete-post'),
    path('users/', views.user_list, name='user-list'),
    path('follow/<int:user_id>/', views.follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow-user'),
]