from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
from .forms import UserRegisterForm, ProfileForm
from django.contrib import messages
from posts.models import Post
from social.models import Follow

# Create your views here.


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            Profile.objects.create(user=user)
            messages.success(request, "Registration successful. Please log in.")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profile", username=user.username)
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(user=user).order_by("-created_at")
    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follow.objects.filter(
            follower=request.user, following=user
        ).exists()
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect("profile", username=username)
    else:
        form = ProfileForm(instance=profile)
    return render(
        request,
        "accounts/profile.html",
        {
            "profile": profile,
            "form": form,
            "posts": posts,
            "is_following": is_following,
        },
    )


@login_required
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)
    if request.user != target_user:
        follow, created = Follow.objects.get_or_create(
            follower=request.user, following=target_user
        )
        if not created:
            follow.delete()  # Unfollow if already following
    return redirect("profile", username=username)
