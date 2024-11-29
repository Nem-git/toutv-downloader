import unidecode
import string

from common.episode import Episode
from common.options import Options
from common.season import Season
from common.show import Show


class Path:

    def Path(self, show: Show, season: Season, episode: Episode, options: Options) -> str:

        title: str = unidecode(show.title)

        path_cleaned_title: str
        for char in title:
            if path_cleaned_title:
                if path_cleaned_title[-1] == ".":
                    char: str = char.capitalize()

                if char in string.whitespace:
                    char: str = "."

            path_cleaned_title += char
        
        # Need to fix language
        path: str = f"{options.download_path}{path_cleaned_title}.S{season.season_number:02}E{episode.episode_number:02}.{episode.language.upper()[:2]}"

        if options.audio_description:
            path += ".AD"
        
        path = f".{options.resolution}p{options.custom_string}"

        return path