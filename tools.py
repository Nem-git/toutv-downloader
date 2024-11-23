import os
import json
import string
from unidecode import unidecode
import subprocess



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
                if filetype == "" or filetype == file[-len(filetype):]:
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



def n_m3u8dl_re_download(options):
    commands = []

    n_m3u8dl_re_video_command = [
        "n-m3u8dl-re",
        options["mpd_url"],
        "--use-shaka-packager",
        "-sv",
        f'res={options["resolution"]}*:for=best',
        "--save-name",
        f'{options["path"]}.dirty'
    ]

    commands.append(n_m3u8dl_re_video_command)


    n_m3u8dl_re_audio_command = [
        "n-m3u8dl-re",
        options["mpd_url"],
        "--use-shaka-packager",
        "-sa",
        f'role="Main":for=best',
        "--save-name",
        options["path"]
    ]

    commands.append(n_m3u8dl_re_audio_command)

    if options["audio_description"]:
        n_m3u8dl_re_audio_description_command = [
            "n-m3u8dl-re",
            options["mpd_url"],
            "--use-shaka-packager",
            "-sa",
            f'role="Alternate":for=best',
            "--save-name",
            f'{options["path"]}.ad'
        ]

        commands.append(n_m3u8dl_re_audio_description_command)

    for command in commands:
        for key in options["decryption_keys"]:
            command.append("--key")
            command.append(key)

        if options["quiet"]:
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(command)

def remove_phantom_subs(options):
    ffmpeg_command = [
        "ffmpeg",
        "-i",
        f'{options["path"]}.dirty.mp4',
        "-map",
        "0",
        "-codec",
        "copy",
        "-bsf:v",
        "filter_units=remove_types=6, filter_units=remove_types=39",
        f'{options["path"]}.mp4',
        "-y"
    ]

    if options["quiet"]:
        subprocess.run(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run(ffmpeg_command)

    
def mkvmerge_merge(options):
    mkvmerge_command = [
        "mkvmerge",
        "-o",
        f'{options["path"]}.mkv',
        "--title",
        options["clean_name"],
        "--default-language",
        options["language"]
    ]

    if options["audio_description"]:
        audio_description_audio = get_downloaded_name(f'{options["path"]}.ad', ".m4a", [])
    
        main_audio = get_downloaded_name(options["path"], ".m4a", audio_description_audio)

    else:
        main_audio = get_downloaded_name(options["path"], ".m4a", [])
    
    if options["subs"]:
        subs = get_downloaded_name(options["path"], ".vtt", [])

    if options["quiet"]:
        mkvmerge_command.append("-q")
    else:
        mkvmerge_command.append("-v")

    track_name = options["language"]

    if options["language"] == "fr-CA":
        track_name = "VFQ"
    
    #VIDEO
    mkvmerge_command.extend(["--original-flag", "0", "--default-track-flag", "0", "--track-name", f'0:original {options["resolution"]}p', f'{options["path"]}.mp4'])

    #AUDIO
    mkvmerge_command.extend(["--original-flag", "0", "--default-track-flag", "0", "--language", f'0:{options["language"]}', "--track-name", f"0:{track_name}", main_audio[0]])
    
    if options["audio_description"]:
        #AUDIODESCRIPTION
        mkvmerge_command.extend(["--visual-impaired-flag", "1", "--default-track-flag", "0:0", "--language", f'0:{options["language"]}', "--track-name", f"0:{track_name} AD", audio_description_audio[0]])

    if options["subs"]:
        if subs != []:
            mkvmerge_command.extend(["--language", f'0:{options["language"].lower()}', "--track-name", f"0:{track_name} ", subs[0]])

    if options["quiet"]:
        subprocess.run(mkvmerge_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run(mkvmerge_command)
    
    delete_files(options["path"], [".mkv"])
