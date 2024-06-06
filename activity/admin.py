from django.contrib import admin

from activity.models import Activity, ScoreBoard, Enrollment, CourseStatus

admin.site.register(Activity)
admin.site.register(ScoreBoard)
admin.site.register(Enrollment)
admin.site.register(CourseStatus)
