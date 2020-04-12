import os
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models import signals
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __repr__(self):
        return f"{self.__class__.__name__}'({self.name})'"

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = RichTextField()
    picture = models.ImageField(
        default='default.png', upload_to=settings.PROJECT_PIC_PATH
    )
    categories = models.ManyToManyField(Category)
    technologies = ArrayField(models.CharField(max_length=100))
    slug = models.SlugField(editable=False)
    url = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __repr__(self):
        return f"{self.__class__.__name__}'({self.name})'"

    def __str__(self):
        return self.name


def project_upload_path(instance, filename):
    return os.path.join(
        settings.PROJECT_PIC_PATH, instance.project.slug, filename
    )


class Screenshot(models.Model):
    picture = models.ImageField(upload_to=project_upload_path)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __repr__(self):
        return f"{self.__class__.__name__}'({self.picture}, {self.project})'"

    def __str__(self):
        return str(self.picture)


@receiver(signals.post_delete, sender=Screenshot)
def auto_delete_pic(sender, instance, **kwargs):
    if instance.picture and os.path.isfile(instance.picture.path):
        os.remove(instance.picture.path)


@receiver(signals.pre_save, sender=Screenshot)
def remove_updated_pic(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old = Screenshot.objects.get(instance.pk).picture
    except Screenshot.DoesNotExist:
        return

    new = instance.picture
    if new != old and os.path.isfile(new):
        os.remove(old)
