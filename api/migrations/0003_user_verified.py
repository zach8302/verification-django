# Generated by Django 4.2.2 on 2023-07-01 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_alter_user_managers"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="verified",
            field=models.BooleanField(default=False),
        ),
    ]
