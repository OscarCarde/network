# Generated by Django 4.2.2 on 2023-07-16 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0007_alter_profile_about"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="content",
            field=models.CharField(max_length=10000),
        ),
    ]
