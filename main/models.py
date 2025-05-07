from django.db import models
from django.contrib.auth.models import User


class Meme(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/', height_field=None, width_field=None, max_length=100)
    uploaded_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Swipe(models.Model):
    SWIPE_CHOICES = (('like', 'Like'), ('dislike', 'Dislike'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    action = models.CharField(choices=SWIPE_CHOICES, max_length=15)
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'meme')

    def __str__(self):
        return f'{self.user.username} {self.action}d {self.meme}'


class SavedMemes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    saved_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'meme')

    def __str__(self):
        return f"{self.user.username} saved {self.meme.title}"


class Matches(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    matched_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name="matched_by")
    similarity_score = models.FloatField(0.0)
    matched_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'matched_with')

    def __str__(self):
        return f"{self.user.username}, matched with {self.matched_with.username}"
