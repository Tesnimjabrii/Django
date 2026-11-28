from django.contrib import admin

from .models import Appointment

# Register your models here.
#admin.site.register(Appointment)

#@admin.register(Appointment)
#class AppointmentAdmin(admin.ModelAdmin):
#    list_display = ('reason', 'status', 'duration_minutes', 'appointment_date')
#admin.site.register(Appointment, AppointmentAdmin)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('reason', 'status', 'duration_minutes', 'appointment_date')
    list_filter = ('status', 'appointment_date')
    list_editable = ('status', )
    search_fields = ('status', 'reason')
    ordering = ('-appointment_date',)
    list_per_page = 2 
    fieldsets = (
        ('Description', {
            'fields': ('reason', 'status', 'prescription')
        }),
        ('Date + Duration', {
            'fields': ('appointment_date', 'duration_minutes')
        }),
        ('Planification',{
            'fields': ("created_at", "updated_at")
        })
    )
    readonly_fields = ('created_at', 'updated_at') 