# Generated by Django 5.0.2 on 2024-04-28 03:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grocery', '0003_alter_item_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='commenter',
            new_name='reviewer',
        ),
    ]
