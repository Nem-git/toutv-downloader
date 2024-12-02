

class Subtitle:

    url: str
    language: str = "Unavailable"
    type: str = "Unavailable"
    custom_string: str = ""
    title: str = "Unavailable"

    # N-m3u8dl-RE filters
    download_filters: str = ""