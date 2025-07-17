from django.conf import settings
from django.db import models

# Create your models here.

class DevTool(models.Model):
    name = models.CharField(max_length=50)
    kind = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Idea(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    description = models.TextField(blank=True)
    interest = models.IntegerField(default=0)  # type: ignore
    devtool = models.ForeignKey(DevTool, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # 찜 기능은 추후 추가

    def __str__(self):
        return self.title

class IdeaStar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'idea')
