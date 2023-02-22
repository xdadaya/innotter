# Generated by Django 4.1.7 on 2023-02-22 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('moderator', 'Moderator'), ('admin', 'Admin')], default='user', max_length=9),
        ),
    ]
