import json
from django.core.management.base import BaseCommand
from .command_helpers import construct_media_metadata, construct_memory, convert_timestamp_to_datetime
from gallery.models import CrossPostSource, Media

class Command(BaseCommand):
    help = 'Import Instagram memories from a JSON file.'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'r') as file:
            data = json.load(file)

        # Iterate over archived post media
        for post in data:
 
            memory = construct_memory(post)

            for media_item in post.get('media', []):
                media_uri = media_item.get('uri')
                media_creation_timestamp = media_item.get('creation_timestamp')
                media_metadata = media_item.get('media_metadata')
                cross_post_source = media_item.get('cross_post_source')

                media_metadata_obj = construct_media_metadata(media_metadata)

                cross_post_source_instance, created = CrossPostSource.objects.get_or_create(
                    source_app=cross_post_source['source_app']
                )

                media_metadata_obj.save()
                Media.objects.create(
                    uri=media_uri,
                    creation_timestamp=convert_timestamp_to_datetime(media_creation_timestamp),
                    title=media_item.get('title', ''),
                    cross_post_source=cross_post_source_instance,
                    media_metadata=media_metadata_obj,
                    is_profile_picture=media_item.get('is_profile_picture', False),
                    is_sensitive=False,
                    memory=memory  # Associate media with memory
                )

            memory.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported Instagram posts as memories.'))
