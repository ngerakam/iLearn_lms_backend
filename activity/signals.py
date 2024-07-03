from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save,post_delete

from .models import ActivityLog, CourseActivity, ModuleActivity, LessonActivity
from authentication.models import *
from course.models import *

####authentication model ##############

@receiver(post_save, sender=User)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"The user '{instance.email}' has been created."
        )
    else:
        ActivityLog.objects.create(
            message=f"The user '{instance.email}' has been updated."
        )

@receiver(post_delete, sender=User)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The user '{instance.email}' has been deleted."
    )

@receiver(post_save, sender=UserLearningPath)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"The user '{instance.user.email}', has a new Learning Path '{instance.learning_path.title}' associated with it."
        )
    else:
        ActivityLog.objects.create(
            message=f"The user '{instance.user.email}', has a Learning Path '{instance.learning_path.title}' associated with it updated."
        )

@receiver(post_delete, sender=UserLearningPath)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The user '{instance.user.email}', has a Learning Path '{instance.learning_path.title}' associated with it deleted."
    )


@receiver(post_save, sender=SiteSetup)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"Your site: '{instance.title}' has been created."
        )
    else:
        ActivityLog.objects.create(
            message=f"Your site: '{instance.title}' has been updated."
        )

@receiver(post_delete, sender=SiteSetup)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"Your site '{instance.title}' has been deleted."
    )


@receiver(post_save, sender=SiteAbout)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"Your site: '{instance.site.title}' about has been created."
        )
    else:
        ActivityLog.objects.create(
            message=f"Your site: '{instance.site.title}' about has been updated."
        )

@receiver(post_delete, sender=SiteSetup)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"Your site: '{instance.site.title}' about has been deleted."
    )

    
@receiver(post_save, sender=SiteAddress)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"Your site: '{instance.site.title}' address has been created."
        )
    else:
        ActivityLog.objects.create(
            message=f"Your site: '{instance.site.title}' address has been updated."
        )

@receiver(post_delete, sender=SiteAddress)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"Your site: '{instance.site.title}' address has been deleted."
    )

#######course model #########


@receiver(post_save, sender=LearningPath)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"A new Learning Path '{instance.title}' has been created."
        )
    else:
        ActivityLog.objects.create(
            message=f"The Learning Path '{instance.title}' has been updated."
        )

@receiver(post_delete, sender=LearningPath)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The Learning Path '{instance.title}' has been deleted."
    )

@receiver(post_save, sender=Category)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"A new Category '{instance.title}' has been created."
        )
    else:
        ActivityLog.objects.create(
            message=f"The Category '{instance.title}' has been updated."
        )

@receiver(post_delete, sender=Category)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The Category '{instance.title}' has been deleted."
    )


@receiver(post_save, sender=Course)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"A new Course '{instance.title}' has been created."
        )
    else:
        ActivityLog.objects.create(
            message=f"The Course '{instance.title}' has been updated."
        )

@receiver(post_delete, sender=Course)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The Course '{instance.title}' has been deleted."
    )

@receiver(post_save, sender=Module)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"A new Module '{instance.title}' has been created for course '{instance.course.title}'."
        )
    else:
        ActivityLog.objects.create(
            message=f"The Module '{instance.title}' has been updated for course '{instance.course.title}'."
        )

@receiver(post_delete, sender=Module)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The Module '{instance.title}' has been deleted for course '{instance.course.title}'."
    )


@receiver(post_save, sender=Lesson)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"A new Lesson '{instance.title}' has been created for Module '{instance.module.title}'."
        )
    else:
        ActivityLog.objects.create(
            message=f"The Lesson '{instance.title}' has been updated for Module '{instance.module.title}'."
        )

@receiver(post_delete, sender=Lesson)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The Lesson '{instance.title}' has been deleted for Module '{instance.module.title}'."
    )

@receiver(post_save, sender=Comment)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"A new Comment '{instance.title}' has been created for course '{instance.course.title}'."
        )
    else:
        ActivityLog.objects.create(
            message=f"The Comment '{instance.title}' has been updated for course '{instance.course.title}'."
        )

@receiver(post_delete, sender=Comment)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The Comment '{instance.title}' has been deleted for course '{instance.course.title}'."
    )


@receiver(post_save, sender=Enrollment)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"A new Enrollment '{instance.id}' has been created for user '{instance.user.email}', and course '{instance.course.title}'."
        )
    else:
        ActivityLog.objects.create(
            message=f"The Enrollment '{instance.id}' has been updated for user '{instance.user.email}', and course '{instance.course.title}'."
        )

@receiver(post_delete, sender=Enrollment)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The Enrollment '{instance.id}' has been deleted for user '{instance.user.email}', and course '{instance.course.title}'."
    )

@receiver(post_save, sender=Progress)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"A new Progress '{instance.id}' has been created for user '{instance.user.email}'."
        )
    else:
        ActivityLog.objects.create(
            message=f"The Progress '{instance.id}' has been updated for user '{instance.user.email}'."
        )

@receiver(post_delete, sender=Progress)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The Progress '{instance.id}' has been deleted for user '{instance.user.email}'."
    )

########## activity models ######

@receiver(post_save, sender=CourseActivity)
@receiver(post_save, sender=ModuleActivity)
@receiver(post_save, sender=LessonActivity)
def log_activity_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"A new {sender.__name__} activity has been created for '{instance.created_by}'."
        )
    else:
        ActivityLog.objects.create(
            message=f"The {sender.__name__} activity for '{instance.created_by}' has been updated."
        )

@receiver(post_delete, sender=CourseActivity)
@receiver(post_delete, sender=ModuleActivity)
@receiver(post_delete, sender=LessonActivity)
def log_activity_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The {sender.__name__} activity for '{instance.created_by}' has been deleted."
    )