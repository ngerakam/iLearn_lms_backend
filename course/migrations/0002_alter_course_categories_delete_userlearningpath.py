# Generated by Django 4.0 on 2024-07-05 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='categories',
            field=models.ManyToManyField(related_name='courses', to='course.Category'),
        ),
        migrations.DeleteModel(
            name='UserLearningPath',
        ),
    ]