from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_post, name="create_post"),
    path("edit/<int:post_id>/", views.edit_post, name="edit_post"),
    path("delete/<int:post_id>/", views.delete_post, name="delete_post"),
    path("like/", views.like_post, name="like_post"),
    path("save/", views.save_post, name="save_post"),
    path("comment/", views.comment_post, name="comment_post"),
    path("saved/", views.saved_posts, name="saved_posts"),
    path("", views.home_view, name="posts-home"),
    path("comments/<int:post_id>/", views.get_post_comments, name="get_post_comments"),
    path("comment/delete/", views.delete_comment, name="delete_comment"),
    # Add post, like, comment, save URLs here
]
