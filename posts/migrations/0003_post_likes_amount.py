# Generated by Django 4.1.7 on 2023-02-24 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_remove_post_likes_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes_amount',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
