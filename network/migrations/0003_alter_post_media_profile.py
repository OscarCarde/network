# Generated by Django 4.2.2 on 2023-07-12 21:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0002_post"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="media",
            field=models.ImageField(blank=True, upload_to="media/post_media"),
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "following",
                    models.ManyToManyField(
                        related_name="follower", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]