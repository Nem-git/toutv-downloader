from typing import Any
import toml

class Options:

    # Options in settings.json
    email: str = "sibapiy973@nausard.com"
    password: str = "sibapiy973@nausard.com"
    wvd_path: str = "device.wvd"
    custom_string: str = ".WEB.H264-NoTag"
    download_path: str = "./"

    # Options using arguments
    resolution: int
    video_codec: str = ""
    audio_codec: str = ""
    quiet: bool = False
    audio_description: bool = False
    latest_episode: bool = False
    subtitles: bool = False

    start_season: int
    start_episode: int
    end_season: int
    end_episode: int
    

    # Options using argument to choose seasons and episodes
    # IDK WHAT TO NAME IT


    # Options about favorite drm techs
    favorite_drms: list[str] = ["dash", "hls", "smooth"]

    # Tier
    tier: str = ""

    # Tokens
    authorization_token: str = ""
    claims_token: str = ""

    # Headers
    headers: dict[str, str] = {}
    license_headers: dict[str, str] = {}

    toml_config = {}


    def Write(self, path: str) -> None:

        # Login
        self.toml_config["login"] = {}
        self.toml_config["login"]["email"] = self.email
        self.toml_config["login"]["password"] = self.password

        # Video File
        self.toml_config["video_file"] = {}
        self.toml_config["video_file"]["custom_string"] = self.custom_string
        self.toml_config["video_file"]["root_download_directory"] = self.download_path
        
        # Widevine Decryption File
        self.toml_config["widevine"] = {}
        self.toml_config["widevine"]["wvd_path"] = self.wvd_path

        # Previous Login Informations
        self.toml_config["previous_login_info"] = {}
        self.toml_config["previous_login_info"]["authorization_token"] = self.authorization_token
        self.toml_config["previous_login_info"]["claims_token"] = self.claims_token


        with open(f"{path}.toml", "wt") as f:
            toml.dump(self.toml_config, f)


    def Load(self, path: str) -> None:
        
        with open(f"{path}.toml", "rt") as f:
            self.toml_config: dict[str, Any] = toml.load(f)

        # Login
        self.email = self.toml_config["login"]["email"]
        self.password = self.toml_config["login"]["password"]

        # Video File
        self.custom_string = self.toml_config["video_file"]["custom_string"]
        self.download_path = self.toml_config["video_file"]["root_download_directory"]

        # Widevine Decryption File
        self.wvd_path = self.toml_config["widevine"]["wvd_path"]

        # Previous Login Informations
        self.authorization_token = self.toml_config["previous_login_info"]["authorization_token"]
        self.claims_token = self.toml_config["previous_login_info"]["claims_token"]