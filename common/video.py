

class Video:

    url: str
    title: str = "Unavailable"
    codec: str = "avc"
    resolution_width: int = 1920
    resolution_height: int = 1080
    bitrate: int = 0
    role: str = "main"
    custom_string: str = ""
    default: bool

    # N-m3u8dl-RE filters
    download_filters: str = ""

    # Filter list for phantom subs
    # filter_units=remove_types={video.filter_unit_type}
    filter_unit: list[str] = ["-bsf:v", "filter_units=remove_types=3, filter_units=remove_types=39"]

    # Decryption informations
    pssh: str
    decryption_keys: list[str]