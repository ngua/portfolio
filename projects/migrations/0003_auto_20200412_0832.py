# Generated by Django 3.0.5 on 2020-04-12 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_screenshot'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='categories',
        ),
        migrations.AddField(
            model_name='project',
            name='categories',
            field=models.ManyToManyField(to='projects.Category'),
        ),
    ]
