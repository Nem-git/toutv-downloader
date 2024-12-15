import argparse
import re

from .options import Options


class Arguments:

    show_name: str
    season_episode: str

    streaming_servie: str

    method: str

    start_season: int = 0
    start_episode: int = 0
    end_season: int = 999
    end_episode: int = 999

    def Parse(self, args: list[str], options: Options) -> None:

        parser: argparse.ArgumentParser = self.Create()

        parsed_args: argparse.Namespace = parser.parse_args()

        if len(args) >= 5:
            self.Seasons_Episodes(args[4])
        
        print(self.start_season, self.start_episode, self.end_season, self.end_episode)

        options.start_season = self.start_season
        options.start_episode = self.start_episode
        options.end_season = self.end_season
        options.end_episode = self.end_episode

        self.show_name = parsed_args.show_name
        self.season_episode = parsed_args.season_episode
        self.streaming_servie = parsed_args.streaming_service

        self.method = parsed_args.method

        options.resolution = parsed_args.resolution
        # Need to add video and audio codec parameters

        options.quiet = parsed_args.quiet
        options.audio_description = parsed_args.audio_description
        options.latest_episode = parsed_args.latest
        options.subtitles = parsed_args.subtitles




    def Create(self) -> argparse.ArgumentParser:

        parser = argparse.ArgumentParser(
            description="Tool to download media from multiple streaming services",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        parser.add_argument(
            "streaming_service",
            help="Chosen streaming service (toutv, crave, noovo)",
            choices=["toutv", "crave", "noovo"],
            type=str
        )

        parser.add_argument(
            "method",
            help="Show informations, list all episodes, connect to the streaming site and download",
            choices=["login", "search", "info", "list", "download"],
        )

        parser.add_argument(
            "show_name",
            help="Show's name (Ex: 'temps de chien')",
            nargs="?",
            type=str
        )

        parser.add_argument(
            "season_episode",
            nargs="?",
            help="Season and episode number (Ex: s1e1-s3e2, s1-s2, s1)",
            type=str,
        )

        #parser.add_argument(
        #    "connect",
        #    help="Connect using the chosen streaming service using the credentials given in the settings file",
        #    action="store_true",
        #    default=False
        #)
        #parser.add_argument(
        #    "search",
        #    help="Search for a show using it's name. This will give back a list of shows that match the pattern (search 'temps de chien')",
        #    action="store_true",
        #    default=True
        #)
        #parser.add_argument(
        #    "list",
        #    help="Lists all the episodes available for a show using the search function (list chien OR list 'temps de chien')",
        #    action="store_true",
        #    default=False
        #)
        #parser.add_argument(
        #    "info",
        #    help="Gives all the information about a show, season or episode using using the search function (info 'temps de chien', info 'temps de chien' s1e4)",
        #    action="store_true",
        #    default=False
        #)
        #parser.add_argument(
        #    "download",
        #    help="Download selected content",
        #    action="store_true",
        #    default=False
        #)
        
        download_group = parser.add_argument_group(
            title="Download",
            description="Arguments for the downloads",
            prefix_chars="-"
        )
        
        download_group.add_argument(
            "-l",
            "--latest",
            help="Downloads only the latest episode",
            action="store_true",
            default=False
        )
        download_group.add_argument(
            "-s",
            "--subtitles",
            help="Downloads all subtitles available",
            action="store_true",
            default=False
        )
        download_group.add_argument(
            "-ad",
            "--audio-description",
            help="Downloads audio description audio",
            action="store_true",
            default=False
        )
        download_group.add_argument(
            "-q",
            "--quiet",
            help="Don't receive output on the terminal",
            action="store_true",
            default=False
        )
        download_group.add_argument(
            "-r",
            "--resolution",
            help="Tries to download video at screen height given",
            action="store",
            default=1080,
            type=int
        )

        return parser




    def Seasons_Episodes(self, arg: str) -> None:

        seasons_episodes: list[tuple[str, str, str, str]] = re.findall(r"^s(\d+)e?(\d*)-?s?(\d*)e?(\d*)$", arg)

        #print(arg, seasons_episodes)

        if len(seasons_episodes) == 0:
            # If there's no agument, then select all the episodes available
            return

        try:
            self.start_season = int(seasons_episodes[0][0])
        except ValueError:
            # If there's no start season then we download everything
            return



        try:
            self.start_episode = int(seasons_episodes[0][1])
        except:
            # If the starting episode is not given, we start at the first episode of the season
            self.start_episode = 0

        try:
            self.end_season = int(seasons_episodes[0][2])
        except ValueError:
            # If the ending season is not given, it must mean that it's the same as the starting season
            self.end_season = self.start_season

        try:
            self.end_episode = int(seasons_episodes[0][3])
        except ValueError:
            if self.end_season == self.start_season:
                # That's when the ending season was also not given
                self.end_episode = self.start_episode
            else:
                # That's when the ending season was given and was different from the starting one
                self.end_episode = 999

        if self.start_season > self.end_season:
            raise ValueError("The starting season needs to be lower than the ending season")

        if self.start_season == self.end_season and self.start_episode > self.end_episode:
            raise ValueError("The starting episode needs to be lower than the ending episode")

        #print(self.start_season, self.start_episode, self.end_season, self.end_episode)

