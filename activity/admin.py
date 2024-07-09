from django.contrib import admin

from course.models import Course,Module,Lesson
from activity.models import ActivityLog, CourseActivity, ModuleActivity, LessonActivity


class CourseActivityAdmin(admin.ModelAdmin):
    list_display = ['created_by','activity_course', 'status', 'get_course']
    search_fields = ['activity_course', 'created_by__email']
    list_filter = ['created_by']
    list_per_page = 10
    def get_course(self,obj):
        return Course.objects.get(id=obj.activity_course.id)
    
    get_course.short_description = 'Course'
class ModuleActivityAdmin(admin.ModelAdmin):
    list_display = ['created_by','activity_module', 'status',]

class LessonActivityAdmin(admin.ModelAdmin):
    list_display = ['created_by','activity_lesson', 'status',]

admin.site.register(ActivityLog)
admin.site.register(CourseActivity,CourseActivityAdmin)
admin.site.register(ModuleActivity,ModuleActivityAdmin)
admin.site.register(LessonActivity,LessonActivityAdmin)
