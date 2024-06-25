from django.contrib import admin

from .models import User, UserProfile, SiteAbout, SiteSetup, SiteAddress

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(SiteAbout)
admin.site.register(SiteSetup)
admin.site.register(SiteAddress)
