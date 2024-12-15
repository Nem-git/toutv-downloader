
import os
from unidecode import unidecode
import string

from common.episode import Episode
from common.options import Options
from common.season import Season
from common.show import Show


class Name:

    codecs: dict[str, str] = {
        "avc": "H264",
        "hevc": "H265",
        "av1": "AV1",
        "aac": "AAC",
        "ac3": "AC3",

    }


    def Find_Filename(self, name: str, filetype: str, folder: str) -> list[str]:
        files: list[str] = []

        for file in os.listdir(folder):
            if os.path.isfile(file):
                if name == file[:len(name)] and (filetype == "" or filetype == file[-len(filetype):]):
                    files.append(file)
        
        return files


    def Remove_Filename(self, name: str, folder: str, filetypes: list[str]):
        
        for file in self.Find_Filename(name, "", folder):
            for filetype in filetypes:
                if file[-len(filetype):] == filetype:
                    os.remove(file)



    def Clean_Filename(self, show: Show, season: Season, episode: Episode, options: Options) -> str:

        title: str = unidecode(show.title)

        path_cleaned_title: str = ""
        for char in title:
            if path_cleaned_title != "":
                if path_cleaned_title[-1] == ".":
                    char: str = char.upper()

                if char in string.whitespace:
                    char: str = "."

            path_cleaned_title += char

        
        # Need to fix language
        path: str = f"{path_cleaned_title}.S{season.season_number:02}E{episode.episode_number:02}.{episode.language}"

        if options.audio_description:
            path += ".AD"
        
        path += f".{episode.selected_video.resolution_height}p.WEB.{self.codecs[episode.selected_video.codec]}{options.custom_string}"

        return path


    def Clean_Name(self, show: Show, season: Season, episode: Episode) -> None:

        # Need to make it so its different if not a series
        name: str = f"{show.title} Season {season.season_number} Episode {episode.episode_number}"
        episode.clean_name = name