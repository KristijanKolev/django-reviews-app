# Generated by Django 4.1 on 2022-08-24 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='user_profile_pics/default-profile-picture.jpg', upload_to='user_profile_pics/'),
        ),
    ]
