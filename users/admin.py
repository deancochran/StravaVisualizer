from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
from activities.models import Activity

# admin.site.unregister(User)

# class InlineActivity(admin.TabularInline):
#     model = Activity

class CustomUserAdmin(UserAdmin):
    list_display =  list(UserAdmin.list_display) + [
        'last_authenticated',
        # 'last_strava_update'
        # 'total_activites'
    ]
    
    # inlines = [
    #     InlineActivity,
    #     ]
    fieldsets = UserAdmin.fieldsets + (
        # (None, {'fields': ('last_authenticated','last_strava_update')}),
        # (None, {'fields': ('last_authenticated','last_strava_update')}),
    )
    # readonly_fields = ('image_tag',) + UserAdmin.readonly_fields

    # def total_activites(self, obj):
    #     return obj.activities.all().count()

admin.site.register(User, CustomUserAdmin)
