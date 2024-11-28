import requests

from show import Show
from season import Season
from episode import Episode
from options import Options

class Info:

    def Shows(self, show: Show) -> Show:
        url: str = f"https://services.radio-canada.ca/ott/catalog/v2/toutv/show/{show.id}?device=web"

        r: requests.Response = requests.get(url)

        while not r.ok:
            r: requests.Response = requests.get(url)
        
        info_response: dict[str, str] = r.json()

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
                episode.enable_audio_description = e["videoDescriptionAvailable"]
                episode.enable_subtitles = e["closedCaptionAvailable"]

                season.episodes.append(episode)
            
            show.seasons.append(season)

        return show
    
    def Episodes(self, episode: Episode, options: Options) -> Episode:
        episode_info_url: str = f"https://services.radio-canada.ca/media/meta/v1/index.ashx?appCode=toutv&idMedia={episode.media_id}&output=jsonObject"

        r: requests.Response = requests.get(episode_info_url)

        while not r.ok:
            r: requests.Response = requests.get(episode_info_url)
        
        episode_info_response: dict[str, str] = r.json()

        episode.title = episode_info_response["Metas"]["Title"]
        # Sometimes there's a description, but I don't know how to get it in the right way
        #episode.description = episode_info_response["Metas"]["Description"]
        episode.duration = episode_info_response["Metas"]["length"]
        episode.age_rating = episode_info_response["Metas"]["Rating"]
        episode.release_year = episode_info_response["Metas"]["Date"][:4]
        episode.server_code = episode_info_response["Metas"]["appCode"]

        # Get captions
        if bool(episode_info_response["Metas"]["EIA608ClosedCaptions"]):
            episode.subtitles_info.append({"url": f"https:{episode_info_response["Metas"]["closedCaption"]}"})
       
        else:
            episode.enable_subtitles = False

        # Get audio description availability
        if not bool(episode_info_response["Metas"]["describedVideo"]):
            episode.enable_audio_description = False

        # Need to find a way to get this the right way
        for tech in episode_info_response["availableTechs"]:
            episode.drm_techs.append(tech["name"])
        
        # Choose DRM Type
        for tech in options.favorite_drms:
            if tech in episode.drm_techs:
                manifest_info_url: str = f"https://services.radio-canada.ca/media/validation/v2/?idMedia={episode.media_id}&appCode={episode.server_code}&tech={episode.drm_tech}&output=json"
                episode.drm_tech = tech

                break
        
        # Request manifest informations
        r: requests.Response = requests.get(manifest_info_url, headers={"Authorization": options.authorization_token, "x-claims-token": options.claims_token})

        while not r.ok:
            r: requests.Response = requests.get(manifest_info_url)
        
        manifest_info_response: dict[str, str] = r.json()

        # Get manifest URL
        episode.url = manifest_info_response["url"]

        # Get resolutions available
        for resolution in manifest_info_response["bitrates"]:
            episode.resolutions.append(resolution["width"])

        # Collect all information about drm services
        for param in manifest_info_response["params"]:
            match param["name"]:

                # Playready DRM
                case "playreadyLicenseUrl":
                    episode.playready_license_url = param["value"]
                case "playreadyAuthToken":
                    episode.playready_request_token = param["value"]
                
                # Widevine DRM
                case "widevineLicenseUrl":
                    episode.widevine_license_url = param["value"]
                case "widevineAuthToken":
                    episode.widevine_request_token = param["value"]
                
                # Fairplay DRM
                case "faiplayLicenseUrl":
                    episode.fairplay_license_url = param["value"]
                case "fairplayCertificatePath":
                    episode.fairplay_certificate_path = param["value"]
                case "fairplayAuthToken":
                    episode.fairplay_request_token = param["value"]
        

        match episode.drm_tech:

            # Playready DRM
            case "smooth":
                episode.license_url = episode.playready_license_url
                episode.request_token = episode.playready_request_token
            
            # Widevine DRM
            # Need to make playready work with dash too
            case "dash":
                episode.license_url = episode.widevine_license_url
                episode.request_token = episode.widevine_request_token

            # Fairplay DRM
            case "hls":
                episode.license_url = episode.fairplay_license_url
                episode.request_token = episode.fairplay_request_token
        
        return episode