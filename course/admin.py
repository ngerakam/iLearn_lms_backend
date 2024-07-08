from django.contrib import admin
from .models import LearningPath, Category, Course, Module, Lesson, Comment, Enrollment, Progress

class LessonCommentInline(admin.TabularInline):
    model = Comment
    raw_id_fields = ['lesson']

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'status', 'lesson_type']
    list_filter = ['status', 'lesson_type']
    search_fields = ['title', 'short_description', 'long_description']
    inlines = [LessonCommentInline]

class CourseAdmin(admin.ModelAdmin):
    list_display = ['title',  'status', 'created_by']

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title',  'is_open', 'course']

admin.site.register(LearningPath)
admin.site.register(Category)
admin.site.register(Course,CourseAdmin)
admin.site.register(Module,ModuleAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Comment)
admin.site.register(Enrollment)
admin.site.register(Progress)
