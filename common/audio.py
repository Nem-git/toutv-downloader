

class Audio:

    url: str
    name: str | None = None
    codec: str | None = None
    bitrate: int | None = None
    language: str | None = None
    custom_string: str | None = None
    audio_description: bool = False
    default: bool = False

    # N-m3u8dl-RE filters
    download_filters: str = ""