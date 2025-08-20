from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    # Explicit "following" relation; reverse side is "followers"
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
        blank=True,
    )

    def follow(self, other: "User"):
        if other != self:
            self.following.add(other)

    def unfollow(self, other: "User"):
        if other != self:
            self.following.remove(other)

    def is_following(self, other: "User") -> bool:
        return self.following.filter(pk=other.pk).exists()

    def __str__(self):
        return self.username
