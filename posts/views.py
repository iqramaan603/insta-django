from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Like, SavedPost, Comment
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_GET

# Create your views here.


def home_view(request):
    return render(request, "home.html")


@login_required
def create_post(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        caption = request.POST.get("caption")
        if image:
            post = Post.objects.create(user=request.user, image=image, caption=caption)
            return redirect("/social/feed/")
    return render(request, "post_create.html")


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == "POST":
        caption = request.POST.get("caption")
        image = request.FILES.get("image")
        if caption:
            post.caption = caption
        if image:
            post.image = image
        post.save()
        return redirect("/social/feed/")
    return render(request, "post_edit.html", {"post": post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("/social/feed/")
    return render(request, "post_delete.html", {"post": post})


@login_required
def like_post(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        liked = True
        if not created:
            like.delete()  # Unlike if already liked
            liked = False
        if request.headers.get("Accept") == "application/json":
            return JsonResponse(
                {"success": True, "liked": liked, "likes": post.like_set.count()}
            )
    return redirect("/social/feed/")


@login_required
def save_post(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        saved, created = SavedPost.objects.get_or_create(user=request.user, post=post)
        is_saved = True
        if not created:
            saved.delete()  # Unsave if already saved
            is_saved = False
        if request.headers.get("Accept") == "application/json":
            return JsonResponse({"success": True, "saved": is_saved})
    return redirect("/social/feed/")


@login_required
def comment_post(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        text = request.POST.get("text")
        post = get_object_or_404(Post, id=post_id)
        if text:
            comment = Comment.objects.create(user=request.user, post=post, text=text)
            if request.headers.get("Accept") == "application/json":
                return JsonResponse(
                    {
                        "success": True,
                        "username": comment.user.username,
                        "text": comment.text,
                        "created_at": comment.created_at.strftime("%b %d, %Y %H:%M"),
                        "comment_id": comment.id,
                    }
                )
    return redirect("/social/feed/")


@login_required
def saved_posts(request):
    saved = (
        SavedPost.objects.filter(user=request.user)
        .select_related("post")
        .order_by("-saved_at")
    )
    posts = [s.post for s in saved]
    return render(request, "saved_posts.html", {"posts": posts})


@require_GET
@login_required
def get_post_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comment_set.select_related("user").order_by("created_at")
    data = [
        {
            "username": c.user.username,
            "text": c.text,
            "created_at": c.created_at.strftime("%b %d, %Y %H:%M"),
            "comment_id": c.id,
        }
        for c in comments
    ]
    return JsonResponse({"success": True, "comments": data})


@login_required
def delete_comment(request):
    if request.method == "POST":
        comment_id = request.POST.get("comment_id")
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user == request.user:
            comment.delete()
            return redirect("/social/feed/")
        else:
            return HttpResponseForbidden("You cannot delete this comment.")
    return redirect("/social/feed/")
