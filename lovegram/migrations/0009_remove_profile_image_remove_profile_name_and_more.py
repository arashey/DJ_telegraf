# Generated by Django 5.1.4 on 2025-01-02 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lovegram', '0008_profile_delete_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='name',
        ),
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
