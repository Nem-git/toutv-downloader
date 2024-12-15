

class Video:

    url: str
    title: str | None = None
    codec: str | None = None
    resolution_width: int | None = None
    resolution_height: int | None = None
    bitrate: int | None = None
    role: str | None = None
    custom_string: str = ""
    default: bool = False

    # N-m3u8dl-RE filters
    download_filters: str = ""

    # Filter list for phantom subs
    # filter_units=remove_types={video.filter_unit_type}
    filter_unit: list[str] = ["-bsf:v", "filter_units=remove_types=6, filter_units=remove_types=39"]

    # Decryption informations
    pssh: str = ""
    decryption_keys: list[str] = []