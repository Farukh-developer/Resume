# Generated by Django 5.1.5 on 2025-03-02 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0005_alter_user_user_role_usertprofile'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UsertProfile',
            new_name='UserProfile',
        ),
    ]
