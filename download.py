

from episode import Episode
from file import File
from options import Options

class Download:

    def Download(self, episode: Episode, options: Options):

        # Makes sure you can download in 1080p without account
        # Should find a regex way to replace it
        episode.url = episode.url.replace("filter=3000", "filter=7000")

        file = File()

        file.pssh = ""