# Generated by Django 3.0.5 on 2020-04-12 10:57

from django.db import migrations, models
import projects.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20200412_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(editable=False),
        ),
        migrations.AlterField(
            model_name='screenshot',
            name='picture',
            field=models.ImageField(upload_to=projects.models.project_upload_path),
        ),
    ]