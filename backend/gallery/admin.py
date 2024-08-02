from django.contrib import admin
from .models import ExifData

@admin.register(ExifData)
class ExifDataAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'camera_position', 'source_type', 'iso', 'focal_length', 'lens_model', 'software', 'scene_type', 'lens_make', 'date_time_digitized', 'date_time_original', 'aperture', 'shutter_speed', 'metering_mode', 'scene_capture_type')
    search_fields = ('device_id', 'camera_position', 'source_type', 'lens_model', 'software', 'lens_make')
    list_filter = ('source_type', 'iso', 'scene_type', 'metering_mode', 'scene_capture_type')  # Add filters for better admin navigation
    date_hierarchy = 'date_time_original'  # Adds a date hierarchy filter based on 'date_time_original'

