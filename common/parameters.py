import argparse

from .options import Options


class Parameters:


    def Parse(args: list[str], options: Options):

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
        download_group = parser.add_argument_group("Download", "Arguments for the downloads", prefix_chars="-")
        
        parser.add_argument("--latest", "-l", help="Select only the latest episode", action="store_true", default=False, type=bool)
        
        
        
        #parser.add

        




    def parse_season_episode(seasons_episodes: str):
        seasons_episodes = seasons_episodes.lower()
        start_season = 0
        end_season = 0
        start_episode = 0
        end_episode = 0


        if "s" in seasons_episodes:
            number_of_s = 0

            for char in seasons_episodes:
                if char == "s":
                    number_of_s += 1

            s_index = seasons_episodes.index("s")
            final_number = ""

            for number in range(s_index + 1, len(seasons_episodes) - s_index):
                try:
                    int(seasons_episodes[number])
                    final_number += seasons_episodes[number]
                except:
                    break
                
                start_season = int(final_number)

            if number_of_s == 2:
                end_season_seasons_episodes = seasons_episodes.split("-")[1]
                s_index = end_season_seasons_episodes.index("s")
                final_number = ""

                for number in range(s_index + 1, len(end_season_seasons_episodes) - s_index):
                    try:
                        int(end_season_seasons_episodes[number])
                        final_number += end_season_seasons_episodes[number]
                    except:
                        break
                    
                    end_season = int(final_number)

                if end_season < start_season:
                    print("You can't have a smaller ending season number than starting season number")
                    exit()
            else:
                end_season = start_season

        else:
            start_episode = 0
            end_season = 999
            start_episode = 0
            end_episode = 999

            return start_season, end_season, start_episode, end_episode


        #EPISODES
        if "e" in seasons_episodes:
            number_of_e = 0

            for char in seasons_episodes:
                if char == "e":
                    number_of_e += 1

            e_index = seasons_episodes.index("e")
            final_number = ""

            # STARTING EPISODE
            for number in range(e_index + 1, len(seasons_episodes)):
                try:
                    int(seasons_episodes[number])
                    final_number += seasons_episodes[number]
                except:
                    break
                
                start_episode = int(final_number)

            # FINAL EPISODE
            if number_of_e == 2:
                end_episode_seasons_episodes = seasons_episodes.split("-")[1]
                e_index = end_episode_seasons_episodes.index("e")
                final_number = ""

                for number in range(e_index + 1, len(end_episode_seasons_episodes)):
                    try:
                        int(end_episode_seasons_episodes[number])
                        final_number += end_episode_seasons_episodes[number]
                    except:
                        break
                    
                    end_episode = int(final_number)

                if start_season == end_season and start_episode > end_episode:
                    print("You can't have a smaller ending episode number than starting episode number in the same season")
                    exit()
            else:
                end_episode = start_episode

        else:
            start_episode = 0
            end_episode = 999

        return start_season, end_season, start_episode, end_episode