import toutv_tokens
import sys
import requests
import tools
import dash
import toutv_tools


def search_shows(query: str, quiet: bool = False) -> None:
    
    url: str = f"https://services.radio-canada.ca/ott/catalog/v1/toutv/search?device=web&pageNumber=1&pageSize=999999999&term={query}"

    resp: dict[str, str] = requests.get(url=url).json()

    results: list[dict[str, str]] = []

    for show in resp["result"]:
        if show["type"] == "Show":
            results.append({show["url"]: show["title"]})

            if not quiet:
                print(f"{show['title']} | {show['url']}")

    return results




def list_episodes(url: str, quiet: bool = False) -> dict[str, str]:
    if not toutv_tools.validate_url(url):
        url = search_shows(url, quiet)
        for key in url[0].keys():
            url = key

    url: str = f"https://services.radio-canada.ca/ott/catalog/v2/toutv/show/{url}?device=web"

    resp = requests.get(url=url).json()

    show = get_show_info(resp)
    
    if not quiet:
        print(resp["title"])
        print("-----------------------------------------------------------------------------------------------------")
        print(resp["description"])
        print("-----------------------------------------------------------------------------------------------------")
        for show_tags in show["tags"]:
            print(show_tags)
        print("-----------------------------------------------------------------------------------------------------")

    show["episodes"] = []

    for season in resp["content"][0]["lineups"]:
        for episode in season["items"]:
            if episode["completionTime"] == 0:
                continue
            
            show_info = get_episodes_info(episode)
            show_info["seasonNumber"] = season["seasonNumber"]
            show_info["seasonTitle"] = season["title"]
            
            show["episodes"].append(show_info)
            
            if not quiet:
                if resp["contentType"] == "Standalone":
                    print(f'{episode["url"]} - {episode["title"]} - {show["country"]}')
                else:
                    print(f'{episode["url"]} - {season["title"]} {episode["title"]}')
                

    return show

def get_show_info(resp):
    show = {}
    show["description"] = resp["description"]
    show["title"] = resp["title"]
    show["contentType"] = resp["contentType"]
    show["requestedType"] = resp["requestedType"]
    show["tags"] = {}
    try:
        show["country"] = resp["structuredMetadata"]["countryOfOrigin"]["name"]
        show["type"] = resp["structuredMetadata"]["@type"]
        for show_tags in resp["navigationFilters"]:
            show["tags"][show_tags["url"]] = show_tags["title"]
    except:
        show["country"] = "unknown"
        show["type"] = "unknown"
    

    if show["contentType"] == "Season":
        show["numberOfEpisodes"] = resp["structuredMetadata"]["numberOfEpisodes"]
        show["numberOfSeasons"] = resp["structuredMetadata"]["numberOfSeasons"]

    else:
        show["numberOfEpisodes"] = 1
        show["numberOfSeasons"] = 1
    
    show["tags"] = {}



    try:
        show["language"] = resp["structuredMetadata"]["inLanguage"]
    except:
        if show["country"] == "Canada":
            show["language"] = "fr-CA"
        else:
            show["language"] = "fr-FR"
    
    return show


def get_episodes_info(episode):
    show_info = {}
    show_info["title"] = episode["title"]
    show_info["completionTime"] = episode["completionTime"]
    try:
        show_info["description"] = episode["description"]
    except:
        show_info["description"] = ""
    
    show_info["episodeNumber"] = episode["episodeNumber"]
    show_info["mediaType"] = episode["mediaType"]
    show_info["idMedia"] = episode["idMedia"]

    return show_info

def get_chosen_episodes(all_episodes, url, start_season, end_season, start_episode, end_episode, allow_trailers, quiet):
    chosen_episodes = show_info(url, quiet)
    chosen_episodes["episodes"] = []

    for episode in all_episodes["episodes"]:
        if int(episode["seasonNumber"]) < start_season:
            continue
        if int(episode["seasonNumber"]) > end_season:
            break
        if int(episode["seasonNumber"]) == end_season and int(episode["episodeNumber"]) > end_episode:
            break
        if int(episode["seasonNumber"]) <= start_season and int(episode["episodeNumber"]) < start_episode:
            continue
        
        if episode["mediaType"] != "Trailer" or allow_trailers:
            chosen_episodes["episodes"].append(episode)
    
    return chosen_episodes
        
        


def show_info(url: str, quiet: bool = False) -> dict[str, str]:
    if not toutv_tools.validate_url(url):
        url = search_shows(url, quiet)
        for key in url[0].keys():
            url = key

    url: str = f"https://services.radio-canada.ca/ott/catalog/v2/toutv/show/{url}?device=web"

    resp = requests.get(url=url).json()

    show = get_show_info(resp)
    
    if not quiet:
        print(f'{show["title"]} [{show["country"]}]')
        print("-----------------------------------------------------------------------------------------------------")
        print(show["description"])
        print("-----------------------------------------------------------------------------------------------------")
        for show_tags in show["tags"]:
            print(show_tags)
        print("-----------------------------------------------------------------------------------------------------")
        print(f"{show['numberOfSeasons']} saisons")
        print(f"{show['numberOfEpisodes']} episodes")
        print("-----------------------------------------------------------------------------------------------------")
        print(show["type"])

    return show


def get_download(url, latest, seasons_episodes, options):
    start_season, end_season, start_episode, end_episode = tools.parse_season_episode(seasons_episodes)
    all_episodes = list_episodes(url, options["quiet"])

    chosen_episodes = {}
    
    if latest:
        chosen_episodes = show_info(url, options["quiet"])
        chosen_episodes["episodes"] = all_episodes["episodes"][-1:]
    
    else:
        chosen_episodes = get_chosen_episodes(all_episodes, url, start_season, end_season, start_episode, end_episode, options["allow_trailers"], options["quiet"])
    
    options["language"] = chosen_episodes["language"]

    options["headers"], options["wvd_path"], custom_string = connect()
    
    #Loops through all the chosen episodes and downloads them all
    for episode in chosen_episodes["episodes"]:
        options["clean_name"] = chosen_episodes["title"]

        if episode["mediaType"] == "Standalone":
            options["clean_name"] = chosen_episodes["title"]
            options["path"] = tools.clean_filename(f'{chosen_episodes["title"]}')
        
        else:
            options["path"] = tools.clean_filename(f'{chosen_episodes["title"]}.S{episode["seasonNumber"]:02}E{episode["episodeNumber"]:02}.{options["language"].upper()[:2]}')
            options["clean_name"] = f'{chosen_episodes["title"]} Saison {episode["seasonNumber"]} Episode {episode["episodeNumber"]}'

        if options["audio_description"]:
            options["path"] += ".AD"
        
        options["path"] += f'.{options["resolution"]}p{custom_string}'

        download_content(episode["idMedia"], options)


def download_content(id: int, options):
    episode_info_url: str = f"https://services.radio-canada.ca/media/validation/v2/?appCode=toutv&connectionType=hd&deviceType=multiams&multibitrate=true&output=json&tech=dash&manifestVersion=2&idMedia={id}"

    r = requests.get(episode_info_url)
    resp = r.json()

    if r.status_code != 200:
        return

    if resp["errorCode"] != 0:
        r = requests.get(episode_info_url, headers=options["headers"])
        resp: dict[str, str] = r.json()
    
    if r.status_code != 200:
        return
    
    if resp["errorCode"] != 0:
        print("Couldnt request using given credentials")
        exit()
    
    fixed_resp = toutv_tools.fix_json(resp)
    
    index_episode_url = f"https://services.radio-canada.ca/media/meta/v1/index.ashx?appCode=toutv&idMedia={id}&output=jsonObject"
    resp = requests.get(index_episode_url).json()

    if resp["Metas"]["EIA608ClosedCaptions"] == "true":
        options["subs_url"] = resp["Metas"]["closedCaptionHTML5"]
    else:
        options["subs"] = False
    
    if resp["Metas"]["describedVideo"] == "false":
        options["audio_description"] = False

    low_res_mpd = fixed_resp["url"]
    mpd_url: str = low_res_mpd.replace("filter=3000", "filter=7000")
    key: str = fixed_resp["widevineAuthToken"]
    licence_url: str = fixed_resp["widevineLicenseUrl"]

    challenge_headers = {"x-dt-auth-token": key}

    options["mpd_url"] = mpd_url
    options["licence_url"] = licence_url
    options["challengeHeaders"] = challenge_headers

    return download_toutv(options)

def download_toutv(options):

    options["pssh"] = dash.get_pssh(options["mpd_url"], options["quiet"])

    options["decryption_keys"] = dash.setup_licence_challenge(options["pssh"], options["licence_url"], options["wvd_path"], options["challengeHeaders"])

    if options["subs"]:
        try:
            vtt_text = requests.get(options["subs_url"]).content
            with open(f"{options['path']}.vtt", "wb") as f:
                f.write(vtt_text)
        except requests.exceptions.MissingSchema:
            options["subs"] = False

    tools.n_m3u8dl_re_download(options)
    tools.remove_phantom_subs(options)
    tools.mkvmerge_merge(options)


def help():
    print(toutv_tools.help_text)
    exit()

def connect():
    settings_path = "settings.json"

    return(toutv_tokens.login(settings_path))

def search(args):
    if len(args) > 2:
        return(search_shows(args[2]))
    else:
        return(search_shows("*"))


def list(args):
    if len(args) > 2:
        if not toutv_tools.validate_url(args[2]):
            url = search_shows(args[2])
            for key in url[0].keys():
                url = key
        return list_episodes(args[2])

def info(args):
    if len(args) > 2:
        if not toutv_tools.validate_url(args[2]):
            url = search_shows(args[2])
            for key in url[0].keys():
                url = key
        return show_info(args[2])
    

def download(args):

        resolution = 1080
        quiet = False
        audiodescription = False
        allow_trailers = False
        latest = False
        subs = False


        if "-r" in args:
            resolution = args[int(args.index("-r") + 1)]
        if "-q" in args:
            quiet = True
        if "-ad" in args:
            audiodescription = True
        if "-t" in args:
            allow_trailers = True
        if "-l" in args:
            latest = True
        if "-s" in args:
            subs = True
        
        seasons_episodes = ""
        if len(args) > 3:
            if args[3][1:] != "-":
                seasons_episodes = args[3]
        
        url = args[2]
        if len(args) > 2:
            if not toutv_tools.validate_url(url):
                url = search_shows(url, quiet)
                for key in url[0].keys():
                    url = key
        
        options = {
            "resolution": resolution,
            "quiet": quiet,
            "audio_description": audiodescription,
            "allow_trailers": allow_trailers,
            "subs": subs
        }
        
        get_download(url, latest, seasons_episodes, options)



            

args = sys.argv

if len(args) < 2:
    print(toutv_tools.help_text)
    
    #args.append("download")
    #args.append("Infoman")
    #args.append("-r")
    #args.append("360")
    #args.append("-l")
    #args.append("-s")
    #args.append("-ad")
    #args.append("-q")
    #args.append("s1-s3")

    #download(args)

    exit()

if args[1] == "help":
    help()



if args[1] == "connect":
    connect()


if args[1] == "search":
    search(args)



if args[1] == "list":
    list(args)
    


if args[1] == "info":
    info(args)

if args[1] == "download":
    download(args)

