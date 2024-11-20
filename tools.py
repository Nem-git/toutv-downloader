import os
import json
import string
from unidecode import unidecode



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


def read_creds_from_file(file_path: str) -> tuple[str, str, str, str]:

    with open(file=file_path, mode="rt") as f:
        js = json.load(f)

    email = js["email"]
    password = js["password"]
    wvd_path = js["wvdPath"]
    custom_string = js["customString"]

    return email, password, wvd_path, custom_string


def delete_files(filename, exceptions):
    known_files = []
    
    for file in get_downloaded_name(filename, "", known_files):
        for exception in exceptions:
            if file[-len(exception):] != exception:
                os.remove(file)

def write_tokens(filename: str, headers: dict) -> None:
    with open(f"{filename}.json", "wt") as f:
        f.write(json.dumps(headers))


def read_tokens(filename) -> tuple[str, str]:
    with open(f"{filename}.json", "rt") as f:
        headers = json.loads(f.read())

    return headers


def get_downloaded_name(filename, filetype, known_files):
    files = []
    for file in os.listdir(os.getcwd()):
        if os.path.isfile(file):
            if filename == file[0: len(filename)] and file not in known_files:
                if filetype == "" or filetype == file[-len(filetype):] and "copy" not in file[-len(filetype) - 5: -len(filetype)]:
                    files.append(file)
    return files


def clean_filename(name: str) -> str:
    try:
        name = unidecode(name)
    except NameError:
        pass

    accepted_charaters = string.ascii_letters + string.digits + "-."
    new_name = ""
    for char in name:
        if char not in accepted_charaters:
            char = ""
        
        if len(new_name) >= 1:
            if new_name[-1] == ".":
                if char in string.ascii_letters:
                    char = char.capitalize()
            
            else:
                if char in string.whitespace:
                    char = "."

        new_name += char
    
    return new_name


