import string
import requests


help_text = """
usage: python toutv.py [help] connect,search,list,info,download [download options]

Allows you to search and download content on Tou.TV

help            show this help message and exit

Ways to represent seasons and episode:
    download stat s01e01
    download \"stat/S01E01\" NOT WORKING
    download \"temps de chien\" (Downloads entire series)
    download \"temps de chien\" s01e01-s01e04 (Downloads all episodes from S1E1 to S1E4)
    download \"temps de chien\" s01 (Downloads entire season)
    download \"temps de chien\" s1-s3 (Downloads all episodes from season 1 to 3)
    download \"temps de chien\" s1-s3e2 (Downloads all episodes from season 1 to season 3 episode 2)
    download \"stat e01\" (Downloads all episode 1 in a series) NOT WORKING



positional arguments:
    connect             Connect using your Tou.tv credentials (You need to enter your credentials in the settings.json file)
    search              Search for a show using it's name (search temps de chien). This will give back a list of shows that match the pattern (search \"temps de chien\")
    list                Lists all the episodes available for a show using it's name or it's "url name" (list chien OR list temps-de-chien)
    info                Gives all the information about a show using it's name or it's "url name" (info temps de chien)
    download            Download a show using it's name or it's "url name" (See the representation of the download commands)

download options:
    -r                  Resolution (Ex: -r 1080 or -r 720)
    -q                  Don't have any output in terminal about what the program is doing
    -ad                 Also downloads the audiodescription audio tracks
    -l                  Downloads the latest episode that was available
    -s                  Downloads subtitles (Doesn't seem like it's working right now, idk why)
    

"""

def fix_json(resp: dict[str, str]) -> dict[str, str]:

    temp: dict[str, str] = {"url": resp["url"]}

    for resp_id in resp["params"]:
        name, value = resp_id.values()
        temp[name] = value

    return temp

def validate_url(url: str) -> bool:
    accepted_characters: str = string.ascii_lowercase + "-" + string.digits
    for char in url:
        if char not in accepted_characters:
            return False
    
    url: str = f"https://services.radio-canada.ca/ott/catalog/v2/toutv/show/{url}?device=web"

    resp = requests.get(url=url)
    if resp.status_code != 200:
        return False

    return True