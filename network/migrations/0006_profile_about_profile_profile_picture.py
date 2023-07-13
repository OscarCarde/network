# Generated by Django 4.2.2 on 2023-07-13 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0005_alter_profile_following"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="about",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="profile_picture",
            field=models.ImageField(blank=True, upload_to="media/profile_pictures"),
        ),
    ]
