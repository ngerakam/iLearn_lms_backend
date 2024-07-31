from django.db import migrations, models
from django.utils.timezone import now
from datetime import time


def convert_time_to_datetime(apps, schema_editor):
    UserQuizSession = apps.get_model('quiz', 'UserQuizSession')
    for session in UserQuizSession.objects.all():
        if session.start and isinstance(session.start, time):
            session.start = now().replace(hour=session.start.hour, minute=session.start.minute, second=session.start.second)
        if session.end and isinstance(session.end, time):
            session.end = now().replace(hour=session.end.hour, minute=session.end.minute, second=session.end.second)
        session.save()

class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_alter_quizattempt_unique_together'),  # Update this to the most recent migration file before your custom one
    ]

    operations = [
        migrations.RunPython(convert_time_to_datetime),
    ]
