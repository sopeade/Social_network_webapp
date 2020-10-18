
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("profile/<username>", views.profile, name="profile"),
    path("change_followers", views.change_followers, name="change_followers"),
    path("following", views.following, name="following"),
    path("post/<post_id>", views.edit, name="edit"),
    path("likes/<post_id>", views.likes, name="likes")

]
