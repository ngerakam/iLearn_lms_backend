# Generated by Django 4.0 on 2024-07-10 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_alter_essayquestionanswer_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquizsession',
            name='current_score',
            field=models.IntegerField(default=0),
        ),
    ]