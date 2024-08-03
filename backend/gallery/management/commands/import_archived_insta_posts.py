from datetime import datetime, timezone
import json
from django.core.management.base import BaseCommand
from gallery.models import ExifData, VideoMetadata, PhotoMetadata, CrossPostSource, MemoryMetadata, Media, Memory

class Command(BaseCommand):
    help = 'Import Instagram memories from a JSON file.'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Path to the JSON file')

    # Convert Unix timestamp to a datetime object
    def convert_timestamp_to_datetime(self,timestamp):
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.isoformat()

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'r') as file:
            data = json.load(file)

        # Iterate over archived post media
        for post in data.get('ig_archived_post_media', []):
            memory_title = post.get('title', '')
            memory_creation_timestamp = post.get('creation_timestamp')

            # Create Memory instance
            memory = Memory.objects.create(
                title=memory_title,
                creation_timestamp=self.convert_timestamp_to_datetime(memory_creation_timestamp)
            )

            for media_item in post.get('media', []):
                media_uri = media_item.get('uri')
                media_creation_timestamp = media_item.get('creation_timestamp')
                media_metadata = media_item.get('media_metadata')
                cross_post_source = media_item.get('cross_post_source')

                # Handle media metadata
                video_metadata = media_metadata.get('video_metadata', None)
                photo_metadata = media_metadata.get('photo_metadata', None)
                exif_data = None

                if video_metadata and 'exif_data' in video_metadata and video_metadata['exif_data']:
                    exif_data = ExifData.objects.create(**video_metadata['exif_data'][0])
                    video_metadata_instance = VideoMetadata.objects.create(
                        exif_data=exif_data,
                        has_camera_metadata=video_metadata.get('has_camera_metadata', False)
                    )
                else:
                    video_metadata_instance = None

                if photo_metadata and 'exif_data' in photo_metadata and photo_metadata['exif_data']:
                    exif_data = ExifData.objects.create(**photo_metadata['exif_data'][0])
                    photo_metadata_instance = PhotoMetadata.objects.create(
                        exif_data=exif_data,
                        has_camera_metadata=photo_metadata.get('has_camera_metadata', False)
                    )
                else:
                    photo_metadata_instance = None

                memory_metadata = MemoryMetadata.objects.create(
                    video_metadata=video_metadata_instance,
                    photo_metadata=photo_metadata_instance
                )

                cross_post_source_instance, created = CrossPostSource.objects.get_or_create(
                    source_app=cross_post_source['source_app']
                )

                Media.objects.create(
                    uri=media_uri,
                    creation_timestamp=self.convert_timestamp_to_datetime(media_creation_timestamp),
                    title=media_item.get('title', ''),
                    cross_post_source=cross_post_source_instance,
                    media_metadata=memory_metadata,
                    is_profile_picture=media_item.get('is_profile_picture', False),
                    is_sensitive=False,
                    memory=memory  # Associate media with memory
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported Instagram memories.'))
