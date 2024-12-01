from common.video import Video
from common.audio import Audio
from common.subtitle import Subtitle

class Episode:
    media_id: str
    title: str = "Title unavailable"
    description: str = "Description unavailable"
    duration: float = 0
    content_type: str
    availability: str
    ad: bool = False
    language: str = "Unavailable"
    age_rating: str = "Unavailable"
    release_year: int = 0
    server_code: str = "Unavailable"
    episode_number: int = 0
    clean_name: str = ""

    # Base path name
    path: str

    # Chosen drm type
    url: str
    licence_url: str
    request_token: str

    # Available drm types
    drm_techs: list[str] = []
    drm_tech: str

    # Microsoft
    playready_licence_url: str
    playready_request_token: str

    # Google
    widevine_licence_url: str
    widevine_request_token: str

    # Apple
    fairplay_licence_url: str
    fairplay_certificate_path: str
    fairplay_request_token: str

    # Videos available
    available_videos: list[Video] = []
    selected_video: Video

    # Audios available
    audio_description_available: bool = False
    available_audios: list[Audio] = []
    selected_audios: list[Audio] = []

    # Subtitles available
    subtitles_available: bool = False
    available_subtitles: list[Subtitle] = []
    selected_subtitles: list[Subtitle] = []

    mpd_content: bytes