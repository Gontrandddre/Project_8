# Generated by Django 3.1.6 on 2021-02-10 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("off", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="user",
            new_name="customuser",
        ),
    ]
