from django.db import models
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save,post_delete
from activity.models import ActivityLog

class Team(models.Model):
    name = models.CharField(max_length=255)
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lead_teams', on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teams')

    def __str__(self):
        return self.name

@receiver(post_save, sender=Team)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"The Team '{instance.name}' has been created."
        )
    else:
        ActivityLog.objects.create(
            message=f"The Team '{instance.name}' has been updated."
        )

@receiver(post_delete, sender=Team)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The Team '{instance.name}' has been deleted."
    )


class Chat(models.Model):
    team = models.ForeignKey(Team, related_name='chats', on_delete=models.CASCADE)
    message = models.TextField()
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} - {self.team}"


@receiver(post_save, sender=Chat)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"The Chat '{instance.id}' from '{instance.sender.email}' has been created."
        )
    else:
        ActivityLog.objects.create(
            message=f"The Chat '{instance.id}' from '{instance.sender.email}' has been updated."
        )

@receiver(post_delete, sender=Chat)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The Chat '{instance.id}' from '{instance.sender.email}' has been deleted."
    )

class SystemNotification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CourseNotification(models.Model):
    course = models.ForeignKey('course.Course', related_name='notifications', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course} - {self.title}"

class LearningPathNotification(models.Model):
    learning_path = models.ForeignKey('course.LearningPath', related_name='notifications', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.learning_path} - {self.title}"

# Signal handlers to create activity logs for notifications
@receiver(post_save, sender=SystemNotification)
@receiver(post_save, sender=CourseNotification)
@receiver(post_save, sender=LearningPathNotification)
def log_notification_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"A new {sender.__name__} '{instance.title}' has been created."
        )
    else:
        ActivityLog.objects.create(
            message=f"The {sender.__name__} '{instance.title}' has been updated."
        )

@receiver(post_delete, sender=SystemNotification)
@receiver(post_delete, sender=CourseNotification)
@receiver(post_delete, sender=LearningPathNotification)
def log_notification_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The {sender.__name__} '{instance.title}' has been deleted."
    )