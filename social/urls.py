from django.urls import path
from . import views

urlpatterns = [
    # Add follow, feed, discover URLs here
    path("feed/", views.feed_view, name="feed"),
    path("suggestions/", views.suggestions_view, name="suggestions"),
    path("follow/", views.follow_user, name="follow_user"),
]
