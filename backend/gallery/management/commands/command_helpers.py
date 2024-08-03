from datetime import datetime, timezone

from gallery.models import ExifData, Memory, PhotoMetadata, VideoMetadata

def parse_date(date_str):
    """
    Converts the date string from the format "%Y:%m:%d %H:%M:%S" to the format "%Y-%m-%d %H:%M:%S".
    This value can be present in exif_data as 'date_time_digitized' or 'date_time_original'
    """
    try:
        return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

def convert_timestamp_to_datetime(timestamp):
        """
        Given a unix timestamp, converts it to a date time UTC object.
        """
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.isoformat()

def construct_memory(data):
    """
    Given media's parent, returns a memory object.
    It gets its title and creation_ts from either itself (if there are multiple medias),
    Or from a media object (in case it's single)
    """
    memory_title=""
    memory_creation_timestamp = 0
    # if there's just one media obj, then it'll contain the title and creation_ts, instead of the parent obj, so we need to handle it.
    if len(data['media'])>1:
        memory_title = data.get('title', '')
        memory_creation_timestamp = data.get('creation_timestamp')
    else:
        media = data.get('media',[])
        memory_title = media.get('title')
        memory_creation_timestamp = media.get('creation_timestamp')

    # Create Memory instance
    memory = Memory.objects.create(
        title=memory_title,
        creation_timestamp=convert_timestamp_to_datetime(memory_creation_timestamp)
    )
    return memory

def handle_photo_metadata(media_metadata):
    """
    photo_metadata is a child of 'media_metadata'.
    We first assign everything to None, and then check if media_metadata object contains video_metadata and exif_data.
    If it does, we check for and convert certain values to make sure it fits our model.
    Return:
        photo_metadata parsing result, which can be None
    """
    photo_metadata = media_metadata.get('photo_metadata', None)
    exif_data = None
    photo_metadata_parsing_result = None
    if photo_metadata and 'exif_data' in photo_metadata and photo_metadata['exif_data']:
                    exif_data = photo_metadata['exif_data'][0]
                    if 'date_time_digitized' in exif_data:
                        exif_data['date_time_digitized'] = parse_date(exif_data['date_time_digitized'])
                    if 'date_time_original' in exif_data:
                        exif_data['date_time_original'] = parse_date(exif_data['date_time_original'])
                    exif_data_instance = ExifData.objects.create(**exif_data)
                    photo_metadata_parsing_result = PhotoMetadata.objects.create(
                        exif_data=exif_data_instance,
                        has_camera_metadata=photo_metadata.get('has_camera_metadata', False)
                    )
    
    return photo_metadata_parsing_result

def handle_video_metadata(media_metadata):
    """
    video_metadata is a child of 'media_metadata'.
    We first assign everything to None, and then check if media_metadata object contains video_metadata and exif_data.
    If it does, we check for and convert certain values to make sure it fits our model.
    Return:
        video_metadata parsing result, which can be None
    """
    video_metadata = media_metadata.get('video_metadata', None)
    exif_data = None
    video_metadata_parsing_result = None

    if video_metadata and 'exif_data' in video_metadata and video_metadata['exif_data']:
        exif_data = video_metadata['exif_data'][0]
        if 'date_time_digitized' in exif_data:
            exif_data['date_time_digitized'] = parse_date(exif_data['date_time_digitized'])
        if 'date_time_original' in exif_data:
            exif_data['date_time_original'] = parse_date(exif_data['date_time_original'])
        exif_data_instance = ExifData.objects.create(**exif_data)
        video_metadata_parsing_result = VideoMetadata.objects.create(
            exif_data=exif_data_instance,
            has_camera_metadata=video_metadata.get('has_camera_metadata', False)
        )

    return video_metadata_parsing_result