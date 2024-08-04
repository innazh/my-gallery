import json
from django.core.management.base import BaseCommand
from .command_helpers import construct_media_metadata, construct_memory, convert_timestamp_to_datetime
from gallery.models import CrossPostSource, Media, Memory

class Command(BaseCommand):
    help = 'Import Instagram stories from a JSON file.'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'r') as file:
            data = json.load(file)

        # Iterate over stories
        # In this case, a 'reel' in json data gets broken down into a "Memory" and a "Media", one to one relationship
        for reels in data.get('ig_reels_media', []):
            for reel in reels.get('media', []):
                reel_title = reel.get('title','')
                reel_creation_timestamp = reel.get('creation_timestamp')
                
                memory = Memory(
                title=reel_title,
                creation_timestamp=convert_timestamp_to_datetime(reel_creation_timestamp),
                type="reel"
                )

                media_uri = reel.get('uri')
                media_metadata = reel.get('media_metadata')
                cross_post_source = reel.get('cross_post_source')

                # Handle media metadata
                media_metadata_obj = construct_media_metadata(media_metadata)

                cross_post_source_instance, created = CrossPostSource.objects.get_or_create(
                    source_app=cross_post_source['source_app']
                )

                media_metadata_obj.save()
                Media.objects.create(
                    uri=media_uri,
                    creation_timestamp=convert_timestamp_to_datetime(reel_creation_timestamp),
                    title=reel.get('title', ''),
                    cross_post_source=cross_post_source_instance,
                    media_metadata=media_metadata_obj,
                    is_profile_picture=reel.get('is_profile_picture', False),
                    is_sensitive=False,
                    memory=memory  # Associate media with memory
                )
                memory.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported Instagram reels as memories.'))