

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
    licence_url: str
    request_token: str

    drm_techs: list[str]
    drm_tech: str

    playready_licence_url: str
    playready_request_token: str

    widevine_licence_url: str
    widevine_request_token: str

    fairplay_licence_url: str
    fairplay_certificate_path: str
    fairplay_request_token: str

    resolutions: list[int]

    audio_info: list[str]

    audio_description_available: bool
    audio_description_info: list[dict[str, str]]

    subtitles_available: bool
    subtitles_info: list[str]

    video_codecs: list[str]
    
    pssh: str
    decryption_keys: list[str]

    path: str