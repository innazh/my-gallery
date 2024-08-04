from django.contrib import admin
from .models import ExifData, VideoMetadata, PhotoMetadata, CrossPostSource, MediaMetadata, Memory, Media

@admin.register(ExifData)
class ExifDataAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'camera_position', 'source_type', 'iso', 'focal_length', 'lens_model', 'software', 'scene_type', 'lens_make', 'date_time_digitized', 'date_time_original', 'aperture', 'shutter_speed', 'metering_mode', 'scene_capture_type')
    search_fields = ('device_id', 'camera_position', 'source_type', 'lens_model', 'software', 'lens_make')
    list_filter = ('source_type', 'iso', 'scene_type', 'metering_mode', 'scene_capture_type')  # Add filters for better admin navigation
    date_hierarchy = 'date_time_original'  # Adds a date hierarchy filter based on 'date_time_original'

@admin.register(VideoMetadata)
class VideoMetadataAdmin(admin.ModelAdmin):
    list_display = ('id', 'has_camera_metadata', 'exif_data')
    list_filter = ('has_camera_metadata',)
    search_fields = ('exif_data__id',)

@admin.register(PhotoMetadata)
class PhotoMetadataAdmin(admin.ModelAdmin):
    list_display = ('id', 'has_camera_metadata', 'exif_data')
    list_filter = ('has_camera_metadata',)
    search_fields = ('exif_data__id',)

@admin.register(CrossPostSource)
class CrossPostSourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'source_app')
    search_fields = ('source_app',)

@admin.register(MediaMetadata)
class MediaMetadataAdmin(admin.ModelAdmin):
    list_display = ('id', 'video_metadata', 'photo_metadata')
    list_filter = ('video_metadata', 'photo_metadata')
    search_fields = ('video_metadata__id', 'photo_metadata__id')

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'uri', 'creation_timestamp', 'title', 'cross_post_source', 'is_profile_picture', 'is_sensitive')
    list_filter = ('is_profile_picture', 'is_sensitive')
    search_fields = ('title', 'uri')

@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'creation_timestamp')
    search_fields = ('title',)
    filter_horizontal = ('media',)
