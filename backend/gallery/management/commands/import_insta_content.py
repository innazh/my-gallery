import json
from django.core.management.base import BaseCommand
from .command_helpers import construct_media_metadata, construct_memory, convert_timestamp_to_datetime
from gallery.models import CrossPostSource, Media, Memory

class Command(BaseCommand):
    IMPORT_TYPES = ["archived", "posts", "stories", "reels", "deleted"]
    help = "This commands handles the import of various instagram content-related jsons."

    def add_arguments(self, parser):
        import_types_help = f'Available import types are: {", ".join(self.IMPORT_TYPES)}'

        parser.add_argument("import-type", choices=self.IMPORT_TYPES, help=import_types_help)
        parser.add_argument('--path', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        import_type = kwargs['import-type']
        
        
        with open(path, 'r') as file:
            data = json.load(file)

        match import_type:
            case "archived":
                self.handle_archived(data)
            case "posts":
                self.handle_posts(data)
            case "stories":
                self.handle_stories(data)
            case "reels":
                self.handle_reels(data)
            case "deleted":
                self.handle_deleted(data)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully imported Instagram {import_type}.'))

    def handle_archived(self, data):
        for post in data.get('ig_archived_post_media', []):

            memory = construct_memory(post)

            for media_item in post.get('media', []):
                media_uri = media_item.get('uri')
                media_creation_timestamp = media_item.get('creation_timestamp')
                media_metadata = media_item.get('media_metadata')
                cross_post_source = media_item.get('cross_post_source')

                # Handle media metadata
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
    
    def handle_posts(self, data):
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
    
    def handle_stories(self, data):
        # Iterate over stories
        # In this case, a 'story' in json data gets broken down into a "Memory" and a "Media", one to one relationship
        for story in data.get('ig_stories', []):
            story_title = story.get('title','')
            story_creation_timestamp = story.get('creation_timestamp')
            
            memory = Memory(
            title=story_title,
            creation_timestamp=convert_timestamp_to_datetime(story_creation_timestamp),
            type="story"
            )

            media_uri = story.get('uri')
            media_metadata = story.get('media_metadata')
            cross_post_source = story.get('cross_post_source')

            # Handle media metadata
            media_metadata_obj = construct_media_metadata(media_metadata)

            cross_post_source_instance, created = CrossPostSource.objects.get_or_create(
                source_app=cross_post_source['source_app']
            )

            media_metadata_obj.save()
            Media.objects.create(
                uri=media_uri,
                creation_timestamp=convert_timestamp_to_datetime(story_creation_timestamp),
                title=story.get('title', ''),
                cross_post_source=cross_post_source_instance,
                media_metadata=media_metadata_obj,
                is_profile_picture=story.get('is_profile_picture', False),
                is_sensitive=False,
                memory=memory  # Associate media with memory
            )
            memory.save()
    
    def handle_reels(self, data):
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
    
    def handle_deleted(self, data):
        for post in data.get('ig_recently_deleted_media', []):

            memory = construct_memory(post)

            for media_item in post.get('media', []):
                media_uri = media_item.get('uri')
                media_creation_timestamp = media_item.get('creation_timestamp')
                media_metadata = media_item.get('media_metadata')
                cross_post_source = media_item.get('cross_post_source')

                # Handle media metadata
                media_metadata_obj = construct_media_metadata(media_metadata)

                cross_post_source_instance, created = CrossPostSource.objects.get_or_create(
                    source_app=cross_post_source['source_app']
                )

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
