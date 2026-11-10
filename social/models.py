from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

# Create your models here.


class Follow(models.Model):
    follower = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")


class Feed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class SuggestionCache(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    suggested_users = models.ManyToManyField(User, related_name="suggested_to")
    updated_at = models.DateTimeField(auto_now=True)
