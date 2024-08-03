from datetime import datetime, timezone
import json
from django.core.management.base import BaseCommand
from .command_helpers import convert_timestamp_to_datetime, handle_photo_metadata, handle_video_metadata
from gallery.models import CrossPostSource, MemoryMetadata, Media, Memory

class Command(BaseCommand):
    help = 'Import Instagram memories from a JSON file.'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'r') as file:
            data = json.load(file)

        # Iterate over archived post media
        for post in data.get('ig_recently_deleted_media', []):

            memory_title=""
            memory_creation_timestamp = 0
            # if there's just one media obj, then it'll contain the title and creation_ts, instead of the parent obj, so we need to handle it.
            if len(post['media'])>1:
                memory_title = post.get('title', '')
                memory_creation_timestamp = post.get('creation_timestamp')
            else:
                media = post.get('media',[])
                memory_title = media[0].get('title')
                memory_creation_timestamp = media[0].get('creation_timestamp')

            # Create Memory instance
            memory = Memory.objects.create(
                title=memory_title,
                creation_timestamp=convert_timestamp_to_datetime(memory_creation_timestamp)
            )

            for media_item in post.get('media', []):
                media_uri = media_item.get('uri')
                media_creation_timestamp = media_item.get('creation_timestamp')
                media_metadata = media_item.get('media_metadata')
                cross_post_source = media_item.get('cross_post_source')

                # Handle media metadata
                photo_metadata_instance = handle_photo_metadata(media_metadata)
                video_metadata_instance = handle_video_metadata(media_metadata)

                memory_metadata = MemoryMetadata.objects.create(
                    video_metadata=video_metadata_instance,
                    photo_metadata=photo_metadata_instance
                )

                cross_post_source_instance, created = CrossPostSource.objects.get_or_create(
                    source_app=cross_post_source['source_app']
                )

                Media.objects.create(
                    uri=media_uri,
                    creation_timestamp=convert_timestamp_to_datetime(media_creation_timestamp),
                    title=media_item.get('title', ''),
                    cross_post_source=cross_post_source_instance,
                    media_metadata=memory_metadata,
                    is_profile_picture=media_item.get('is_profile_picture', False),
                    is_sensitive=False,
                    memory=memory  # Associate media with memory
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported Instagram memories.'))