# Generated by Django 2.2.16 on 2022-06-17 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220618_0124'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='title_id',
            new_name='title',
        ),
    ]
