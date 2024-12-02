

class Audio:

    url: str = ""
    name: str = ""
    codec: str = "aac"
    bitrate: int = 0
    language: str = "Unavailable"
    custom_string: str = ""
    audio_description: bool = False
    default: bool = False

    # N-m3u8dl-RE filters
    download_filters: str = ""