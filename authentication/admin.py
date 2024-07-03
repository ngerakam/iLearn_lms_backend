from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, UserProfile, SiteAbout, SiteSetup, SiteAddress, UserLearningPath

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'get_groups')

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    
    get_groups.short_description = 'Groups'

admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(UserLearningPath)
admin.site.register(SiteAbout)
admin.site.register(SiteSetup)
admin.site.register(SiteAddress)
