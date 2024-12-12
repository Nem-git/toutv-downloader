import argparse
import re

from .options import Options


class Parameters:


    def Parse(self, args: list[str], options: Options):

        # Parameters using -
        
        for arg in args:
            if arg == "-r":
                try:
                    options.resolution = int(args[args.index(arg) + 1])
                except:
                    raise ValueError("The resolution given after the -r argument is not an integer")
            
            if arg == "-s":
                options.subtitles = True
            
            if arg == "-l":
                options.latest_episode = True
            
            if arg == "-ad":
                options.audio_description = True
        
        parser = argparse.ArgumentParser(description="Tool to download media from multiple online services")
        
        parser.add_argument("download")
        
        
        download_group = parser.add_argument_group("Download", "Arguments for the downloads", prefix_chars="-")
        
        download_group.add_argument("--latest", "-l", help="Downloads only the latest episode", action="store_true", default=False, type=bool, required="download" in args)
        download_group.add_argument("--subtitles", "-s", help="Downloads all subtitles available", action="store_true", default=False, type=bool, required="download" in args)
        download_group.add_argument("--audio-description", "-ad", help="Downloads audio description audio", action="store_true", default=False, type=bool, required="download" in args)
        download_group.add_argument("--quiet", "-q", help="Don't receive output on the terminal", action="store_true", default=False, type=bool, required="download" in args)
        download_group.add_argument("--resolution", "-r", help="Tries to download video at screen height given", action="store", default=1080, type=int, required="download" in args)
        


        #parser.add

        




    def parse_season_episode(seasons_episodes: str):

        # ^s(\d+)
        # Search for a season number
        # e?(\d+)?
        # Search for an episode number
        # -?s?(\d+)?
        # Search for the ending season
        # e?(\d+)?
        # Search for the ending episode

        seasons_episodes: list[tuple[str]] = re.findall(r"^s(\d+)e?(\d+)?-?s?(\d+)?e?(\d+)?$", seasons_episodes)

        if len(seasons_episodes) < 4:
            return None

        start_season = seasons_episodes[0][0]
        start_episode = seasons_episodes[0][1]
        end_season = seasons_episodes[0][2]
        end_episode = seasons_episodes[0][3]
        
        if start_episode == "":
            start_episode = 0
        
        if end_season == "":
            end_season = 999
        
        if end_episode == "":
            end_episode = 999

        return start_season, end_season, start_episode, end_episode