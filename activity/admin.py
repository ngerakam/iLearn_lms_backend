from django.contrib import admin

from activity.models import ActivityLog, CourseActivity, ModuleActivity, LessonActivity

admin.site.register(ActivityLog)
admin.site.register(CourseActivity)
admin.site.register(ModuleActivity)
admin.site.register(LessonActivity)
