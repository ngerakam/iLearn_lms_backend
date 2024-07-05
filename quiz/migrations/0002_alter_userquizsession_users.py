# Generated by Django 4.0 on 2024-07-05 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_user_groups_alter_user_user_permissions_and_more'),
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquizsession',
            name='users',
            field=models.ManyToManyField(related_name='sessions', to='authentication.User'),
        ),
    ]