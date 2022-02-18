
from django.contrib import admin
from activities.models import Activity

class ActivityAdmin(admin.ModelAdmin):
    list_display =  [
        'id',
        'user',
        'name',
        'type',
        'distance',
    ]

    fieldsets = (
        ('Activity Info', {'fields': ('activity_id','name','type','distance','elapsed_time')}),
        ('Time', {'fields': ('start_date','start_date_local','timezone','utc_offset')}),
        ('Location', {'fields': ('location_city','location_state','location_country')}),
        ('Map', {'fields': ('start_latitude','start_longitude','start_latlng','end_latlng','map_latitude','map_longitude','map_elevation')}),
        ('Achievements', {'fields': ('achievement_count','kudo_count','comment_count','pr_count')}),
        ('Activity Stats', {'fields': ('average_cadence','average_heartrate','average_speed','elevation_high','elevation_low',
        'max_heartrate','max_speed','moving_time','suffer_score','total_elevation_gain')}),
        # (None, {'fields': ('last_authenticated','last_strava_update')}),
    )
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Activity, ActivityAdmin)
