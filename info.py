import requests

from show import Show
from season import Season
from episode import Episode

class Info:

    def Shows(self, show: Show):
        url: str = f"https://services.radio-canada.ca/ott/catalog/v2/toutv/show/{show.id}?device=web"

        r: requests.Response = requests.get(url)

        while not r.ok:
            r: requests.Response = requests.get(url)
        
        info_response = r.json()

        show.description = info_response["description"]
        show.content_type = info_response["contentType"]
        show.language = info_response["structuredMetadata"]["inLanguage"]
        show.country = info_response["structuredMetadata"]["countryOfOrigin"]["name"]
        show.seasons = []

        for s in info_response["content"][0]["lineups"]:
            season = Season()

            season.id = s["url"]
            season.title = s["title"]
            season.season_number = s["seasonNumber"]
            season.availability = s["tier"]
            season.episodes = []

            for e in s["items"]:
                episode = Episode()

                episode.media_id = e["idMedia"]
                episode.title = e["title"]
                episode.description = e["description"]
                episode.duration = e["metadata"]["duration"]
                episode.content_type = e["mediaType"]
                episode.availability = e["tier"]
                episode.ad = episode.content_type == "Trailer"
                episode.episode_number = e["episodeNumber"]
                episode.audio_description = e["videoDescriptionAvailable"]
                episode.subtitles = e["closedCaptionAvailable"]

                season.episodes.append(episode)
            
            show.seasons.append(season)

        return show