from django.db import models
from django.contrib.postgres.fields import ArrayField
from ckeditor.fields import RichTextField


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextField()
    picture = models.ImageField(default='default.png', upload_to='projects')
    categories = ArrayField(models.CharField(max_length=100))
    technologies = ArrayField(models.CharField(max_length=100))

    def __str__(self):
        return self.name
