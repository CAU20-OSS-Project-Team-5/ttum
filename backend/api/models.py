from django.db import models


# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=1000)
    images = models.ImageField(blank=True, upload_to="images", null=True)
    image_name = models.CharField(max_length=200, null=True)
    _type = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.title
