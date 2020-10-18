from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    num_followers = models.IntegerField(default=0)
    num_following = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.username}"


class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now=True)
    like_count = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.post}"

    def serialize(self):
        return {
            "id": self.id,
            "post": self.post,
            "timestamp": self.timestamp.strftime("%m %d %Y, %I:%M %p")
        }


class ListFollowed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    people_followed = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="the_followed")

    def __str__(self):
        return f"{self.people_followed}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_posts = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    like_unlike = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} likes {self.liked_posts}"
