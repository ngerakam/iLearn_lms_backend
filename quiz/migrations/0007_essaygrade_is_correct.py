# Generated by Django 4.0 on 2024-08-01 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_essaygrade_quizattempt_quiz_time_limit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='essaygrade',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
    ]