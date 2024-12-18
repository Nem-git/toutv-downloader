import requests

import common

class Info:

    def Show(self, show: common.Show) -> None:
        url: str = f"https://services.radio-canada.ca/ott/catalog/v2/toutv/show/{show.id}?device=web"

        r: requests.Response = requests.get(url)

        while not r.ok:
            r: requests.Response = requests.get(url)
        
        info_response = r.json()

        show.title = info_response["title"]
        show.description = info_response["description"]
        show.content_type = info_response["contentType"]
        try:
            show.language = info_response["structuredMetadata"]["inLanguage"]
        except:
            show.language = "und"
        
        try:
            show.country = info_response["structuredMetadata"]["countryOfOrigin"]["name"]
        except:
            show.country = "und"
        
        show.seasons = []

        for s in info_response["content"][0]["lineups"]:
            season = common.Season()

            season.id = s["url"]
            season.title = s["title"]
            season.season_number = s["seasonNumber"]
            season.availability = s["tier"]
            season.episodes = []

            for e in s["items"]:
                episode = common.Episode()

                episode.media_id = e["idMedia"]
                episode.title = e["title"]
                if "description" in e.keys():
                    episode.description = e["description"]
                episode.duration = e["metadata"]["duration"]
                episode.content_type = e["mediaType"]
                episode.availability = e["tier"]
                episode.ad = episode.content_type == "Trailer"
                episode.episode_number = e["episodeNumber"]
                episode.audio_description_available = e["videoDescriptionAvailable"]
                episode.subtitles_available = e["closedCaptionAvailable"]

                season.episodes.append(episode)
            
            show.seasons.append(season)
    
    def Episodes(self, episode: common.Episode, options: common.Options) -> None:
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
        episode.available_subtitles = []
        if bool(episode_info_response["Metas"]["EIA608ClosedCaptions"]):
            subtitle: common.Subtitle = common.Subtitle()
            subtitle.url = f"https:{episode_info_response["Metas"]["closedCaption"]}"

            if subtitle.url[-4:] == ".vtt":
                subtitle.type = "VTT"
            else:
                subtitle.type = "SRT"
            
            episode.available_subtitles.append(subtitle)

        else:
            episode.subtitles_available = False

        # Get audio description availability
        if not bool(episode_info_response["Metas"]["describedVideo"]):
            episode.audio_description_available = False

        # Need to find a way to get this the right way
        episode.drm_techs = []
        for tech in episode_info_response["availableTechs"]:
            episode.drm_techs.append(tech["name"])
        
        # Choose DRM Type
        for tech in options.favorite_drms:
            if tech in episode.drm_techs:
                episode.drm_tech = tech
                manifest_info_url: str = f"https://services.radio-canada.ca/media/validation/v2/?idMedia={episode.media_id}&appCode={episode.server_code}&tech={episode.drm_tech}&output=json"

                break
        
        # Request manifest informations
        r: requests.Response = requests.get(manifest_info_url, headers=options.headers)

        while not r.ok:
            r: requests.Response = requests.get(manifest_info_url, headers=options.headers)
        
        manifest_info_response: dict[str, str | int] = r.json()

        if manifest_info_response["errorCode"] != 0:
            raise requests.RequestException("Your account doesn't have the right to access this content")

        # Get manifest URL
        episode.url = manifest_info_response["url"]

        # Makes sure you can download in 1080p without account
        # Maybe should find a regex way to replace it
        episode.url = episode.url.replace("filter=3000", "filter=7000")

        # Get resolutions available
        episode.available_videos = []
        for resolution in manifest_info_response["bitrates"]:
            video: common.Video = common.Video()
            video.bitrate = resolution["bitrate"]
            video.resolution_width = resolution["width"]
            video.resolution_height = resolution["height"]
            
            episode.available_videos.append(video)

        # Collect all information about drm services
        for param in manifest_info_response["params"]:
            match param["name"]:

                # Playready DRM
                case "playreadyLicenseUrl":
                    episode.playready_licence_url = param["value"]
                case "playreadyAuthToken":
                    episode.playready_request_token = param["value"]
                
                # Widevine DRM
                case "widevineLicenseUrl":
                    episode.widevine_licence_url = param["value"]
                case "widevineAuthToken":
                    episode.widevine_request_token = param["value"]
                
                # Fairplay DRM
                case "faiplayLicenseUrl":
                    episode.fairplay_licence_url = param["value"]
                case "fairplayCertificatePath":
                    episode.fairplay_certificate_path = param["value"]
                case "fairplayAuthToken":
                    episode.fairplay_request_token = param["value"]
        

        match episode.drm_tech:

            # Playready DRM
            case "smooth":
                episode.licence_url = episode.playready_licence_url
                episode.request_token = episode.playready_request_token
            
            # Widevine DRM
            # Need to make playready work with dash too
            case "dash":
                episode.licence_url = episode.widevine_licence_url
                episode.request_token = episode.widevine_request_token

            # Fairplay DRM
            case "hls":
                episode.licence_url = episode.fairplay_licence_url
                episode.request_token = episode.fairplay_request_token