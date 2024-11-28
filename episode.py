

class Episode:
    media_id: str
    title: str
    description: str
    duration: float
    content_type: str
    availability: str
    ad: bool
    age_rating: str
    release_year: int
    server_code: str
    episode_number: int

    url: str
    license_url: str
    request_token: str

    drm_techs: list[str]
    drm_tech: str

    playready_license_url: str
    playready_request_token: str

    widevine_license_url: str
    widevine_request_token: str

    fairplay_license_url: str
    fairplay_certificate_path: str
    fairplay_request_token: str

    resolutions: list[str]

    audio_info: list[str]

    enable_audio_description: bool
    audio_description_info: list[dict[str, str]]

    enable_subtitles: bool
    subtitles_info: list[str]

    video_codecs: list[str]
    