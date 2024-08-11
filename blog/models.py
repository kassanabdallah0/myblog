from django.db import models
import os
from django.conf import settings

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='articles/')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            # Check if the object already exists in the database
            this = Article.objects.get(id=self.id)
            if this.image != self.image:
                # If the image is different, delete the old one
                if os.path.isfile(this.image.path):
                    os.remove(this.image.path)
        except:
            pass  # This is a new object, so there's no old image to delete
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)


class Event(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='events/')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            # Check if the object already exists in the database
            this = Event.objects.get(id=self.id)
            if this.image != self.image:
                # If the image is different, delete the old one
                if os.path.isfile(this.image.path):
                    os.remove(this.image.path)
        except:
            pass  # This is a new object, so there's no old image to delete
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
