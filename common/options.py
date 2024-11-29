

class Options:

    # Options in settings.json
    email: str
    password: str
    wvd_path: str = "device.wvd"
    custom_string: str = ".WEB.H264-NoTag"
    download_path: str = "./"

    # Options using arguments
    resolution: int = 1080
    quiet: bool = False
    audio_description: bool = False
    allow_ads: bool = False
    latest_episode: bool = False
    subtitles: bool = False

    # Options using argument to choose seasons and episodes
    # IDK WHAT TO NAME IT


    # Options about favorite drm techs
    favorite_drms = ["dash", "hls", "smooth"]

    # Tokens
    authorization_token: str
    claims_token: str
