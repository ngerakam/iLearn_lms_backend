# Generated by Django 4.0 on 2024-07-10 15:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0003_essayquestionanswer_created_by'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='essayquestionanswer',
            unique_together={('created_by', 'essay_question')},
        ),
    ]
