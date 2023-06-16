from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from .models import providerSchedule , Service_category ,ReservationInfo
class providerschAdmin (admin.ModelAdmin):
    filter_horizontal=()
    list_filter= ()
    fieldsets=()
    list_display = ('id','provider','get_timeslots')
    
    def get_timeslots(self, obj):
        timeslots = obj.TimeSlot.all()
        timeslot_strings = [f"{slot.start_time} - {slot.end_time}<br>" for slot in timeslots]
        return mark_safe(''.join(timeslot_strings))

admin.site.register(providerSchedule,providerschAdmin)   



class ReservationInfoAdmin (admin.ModelAdmin):
    filter_horizontal=()
    list_filter= ()
    fieldsets=()
    list_display = ('id','recipient','service_Info',
                    'start_time','end_time')
    
admin.site.register(ReservationInfo,ReservationInfoAdmin) 


class servicecategoryAdmin (admin.ModelAdmin):
    filter_horizontal=()
    list_filter= ()
    fieldsets=()
    list_display = ('id','category')
    
admin.site.register(Service_category,servicecategoryAdmin)   

# Register your models here.
