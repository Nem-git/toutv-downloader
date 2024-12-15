

class Subtitle:

    url: str = ""
    language: str | None = None
    type: str = ""
    custom_string: str = ""
    title: str | None = None

    # N-m3u8dl-RE filters
    download_filters: str = ""