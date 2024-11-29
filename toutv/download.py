

from common.show import Show
from common.season import Season
from common.episode import Episode
from common.options import Options
from common.pssh import Pssh
from common.widevine import Widevine
from common.path import Path

class Download:

    def Download(self, show: Show, season: Season, episode: Episode, options: Options):

        # Makes sure you can download in 1080p without account
        # Should find a regex way to replace it
        episode.url = episode.url.replace("filter=3000", "filter=7000")

        episode.pssh = Pssh().Get(episode)

        episode.decryption_keys = Widevine().Challenge(episode, options)

        episode.path = Path().Path(show, season, episode, options)

        headers: dict[str, str] = {"x-dt-auth-token": episode.request_token}

    

    def Subtitles(self, episode: Episode):
        