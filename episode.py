

class Episode:
    media_id: str
    title: str
    description: str
    duration: float
    content_type: str
    availability: str
    ad: bool
    episode_number: int

    reolutions: list[str]

    audio_description: bool
    audio_description_languages: list[str]

    subtitles: bool
    subtitles_languages: list[str]

    video_codecs: list[str]
    