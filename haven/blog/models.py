from django.db import models
from autoslug import AutoSlugField
from django.conf import settings

class Post(models.Model):
    title=models.CharField(max_length=200)
    body=models.TextField()
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False)
    date=models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(default='fallback.png', blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='posts', null=True)

    class Meta:
        db_table = 'blog_posts'

    def __str__(self):
        return self.title

class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
