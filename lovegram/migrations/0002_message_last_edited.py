# Generated by Django 5.1.4 on 2025-01-01 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lovegram', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='last_edited',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
