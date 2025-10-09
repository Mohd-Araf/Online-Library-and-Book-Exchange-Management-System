from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(blank=True, null=True)

    # optional stats (future use)
    total_exchanges = models.PositiveIntegerField(default=0)
    total_purchases = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        try:
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:   # quality improve
                new_img = (300, 300)
                img.thumbnail(new_img)
                img.save(self.avatar.path)
        except Exception as e:
            print("Image resize error:", e)
