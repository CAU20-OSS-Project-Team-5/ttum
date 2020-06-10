from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200)
    images = models.ImageField(blank=True, upload_to="images", null=True)
    
    def __str__(self):
        return self.title

