from django.db import models

# Create your models here.
class ExifData(models.Model):
    device_id = models.CharField(max_length=100, null=True, blank=True)
    camera_position = models.CharField(max_length=10, null=True, blank=True)
    source_type = models.CharField(max_length=10, null=True, blank=True)
    iso = models.IntegerField(null=True, blank=True)
    focal_length = models.CharField(max_length=10, null=True, blank=True)
    lens_model = models.CharField(max_length=100, null=True, blank=True)
    software = models.CharField(max_length=20, null=True, blank=True)
    scene_type = models.IntegerField(null=True, blank=True)
    lens_make = models.CharField(max_length=50, null=True, blank=True)
    date_time_digitized = models.DateTimeField(null=True, blank=True)
    date_time_original = models.DateTimeField(null=True, blank=True)
    aperture = models.CharField(max_length=10, null=True, blank=True)
    shutter_speed = models.CharField(max_length=20, null=True, blank=True)
    metering_mode = models.IntegerField(null=True, blank=True)
    scene_capture_type = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

class VideoMetadata(models.Model):
    exif_data = models.ForeignKey(ExifData, on_delete=models.CASCADE, related_name='video_metadata', null=True, blank=True)
    has_camera_metadata = models.BooleanField()

class PhotoMetadata(models.Model):
    exif_data = models.ForeignKey(ExifData, on_delete=models.CASCADE, related_name='photo_metadata', null=True, blank=True)
    has_camera_metadata = models.BooleanField()

class CrossPostSource(models.Model):
    source_app = models.CharField(max_length=10)

class MediaMetadata(models.Model):
    video_metadata = models.ForeignKey(VideoMetadata, on_delete=models.CASCADE, null=True, blank=True)
    photo_metadata = models.ForeignKey(PhotoMetadata, on_delete=models.CASCADE, null=True, blank=True)

class Media(models.Model):
    uri = models.CharField(max_length=255)
    creation_timestamp = models.DateTimeField()
    title = models.TextField(null=True, blank=True)
    cross_post_source = models.ForeignKey(CrossPostSource, on_delete=models.CASCADE)
    media_metadata = models.ForeignKey(MediaMetadata, on_delete=models.CASCADE)
    is_profile_picture = models.BooleanField(default=False) # haven't seen this yet

    is_sensitive = models.BooleanField(default=False)

#any sort of post is a memory, a memory consists of media
class Memory(models.Model):
    media = models.ManyToManyField(Media)
    title = models.CharField(max_length=255)
    creation_timestamp = models.DateTimeField()

    MEMORY_TYPES = [
        ("story", "Story"),
        ("post", "Post")
    ]
    type = models.CharField(max_length=12, choices=MEMORY_TYPES, default=MEMORY_TYPES[1])
    is_sensitive = models.BooleanField(default=False)

#Story will prob be eliminated, and become 'Media' as well. Maybe... i'll add media type there
class Story(models.Model):
    uri = models.URLField()
    creation_timestamp = models.DateTimeField()
    title = models.CharField(max_length=255, blank=True)
    cross_post_source = models.ForeignKey(CrossPostSource, on_delete=models.CASCADE)
    media_metadata = models.OneToOneField(MediaMetadata, on_delete=models.CASCADE)

    is_sensitive = models.BooleanField(default=True)
