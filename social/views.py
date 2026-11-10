from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from posts.models import Post, Like, Comment, SavedPost
from .models import Follow
from django.contrib.auth.models import User

# Create your views here.


@login_required
def feed_view(request):
    # Get users the current user follows
    following = Follow.objects.filter(follower=request.user).values_list(
        "following", flat=True
    )
    if following:
        posts = Post.objects.filter(user__in=following).order_by("-created_at")
    else:
        posts = Post.objects.all().order_by("-created_at")[
            :10
        ]  # Show recent posts if not following anyone
    # Get likes, saved posts, and comments for the current user
    liked_post_ids = Like.objects.filter(user=request.user, post__in=posts).values_list(
        "post_id", flat=True
    )
    saved_post_ids = SavedPost.objects.filter(
        user=request.user, post__in=posts
    ).values_list("post_id", flat=True)
    comments = Comment.objects.filter(post__in=posts)
    return render(
        request,
        "social_feed.html",
        {
            "posts": posts,
            "liked_post_ids": liked_post_ids,
            "saved_post_ids": saved_post_ids,
            "comments": comments,
        },
    )


@login_required
def suggestions_view(request):
    following = Follow.objects.filter(follower=request.user).values_list(
        "following", flat=True
    )
    suggested_users = User.objects.exclude(id__in=following).exclude(id=request.user.id)
    return render(
        request, "social_suggestions.html", {"suggested_users": suggested_users}
    )


@login_required
def follow_user(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        to_follow = User.objects.get(id=user_id)
        Follow.objects.get_or_create(follower=request.user, following=to_follow)
    return redirect("suggestions")
