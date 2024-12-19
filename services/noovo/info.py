
import json
import requests

import common
from common.audio import Audio
from common.subtitle import Subtitle


class Info:

    def Show(self, show: common.Show) -> None:
        url: str = "https://www.noovo.ca/space-graphql/apq/graphql"

        graphql_operation_name = "axisMedia"

        graphql_variables: dict[str, str | list[str] | None] = {
		    "authenticationState": "UNAUTH",
		    "axisMediaId": f"contentid/axis-media-{show.id}",
		    "language": "FRENCH",
		    "maturity": "ADULT",
		    "playbackLanguage": "FRENCH",
		    "subscriptions": [
		        "CANAL_D",
		        "CANAL_VIE",
		        "INVESTIGATION",
		        "NOOVO",
		        "Z"
		    ]
        }

        graphql_query: str = """
query axisMedia($axisMediaId: ID!, $subscriptions: [Subscription]!, $maturity: Maturity!, $language: Language!, $authenticationState: AuthenticationState!, $playbackLanguage: PlaybackLanguage!) @uaContext(subscriptions: $subscriptions, maturity: $maturity, language: $language, authenticationState: $authenticationState, playbackLanguage: $playbackLanguage) {
    contentData: axisMedia(id: $axisMediaId) {
        title
        description
        mediaType
        firstAirYear
        originalSpokenLanguage
        heroBrandLogoId
        agvotCode
        qfrCode
        genres {
            name
        }
        adUnit {
            heroBrand
            product
        }
        mediaConstraint {
            hasConstraintsNow
        }
        cast {
            role
            castMembers {
                fullName
            }
        }
        normalizedRatingCodes {
            language
        }
        seasons {
            title
            id
            seasonNumber
        }
    }
}


"""
        data: dict[str, str | dict[str, str | list[str] | None]] = {
            "operationName": graphql_operation_name,
            "query": graphql_query,
            "variables": graphql_variables,
        }

        headers: dict[str, str] = {
            "content-type": "application/json"
        }

        r: requests.Response = requests.post(url, headers=headers, data=json.dumps(data))

        resp = r.json()
        with open("show.json", "wt") as f:
                f.write(json.dumps(resp))
            
        content_data = resp["data"]["contentData"]

        show.title = content_data["title"]
        show.description = content_data["description"]
        show.content_type = content_data["mediaType"]
        show.release_year = content_data["firstAirYear"]
        show.age_rating = content_data["agvotCode"]

        if content_data["mediaConstraint"]["hasConstraintsNow"]:
            show.availability = "Premium"
        else:
            show.availability = "Free"
        
        show.language = content_data["normalizedRatingCodes"][0]["language"]
        
        show.seasons = []

        # ADD SUPPORT FOR SHOWS WITHOUT SEASONS

        if content_data["seasons"][0]["seasonNumber"] < content_data["seasons"][-1]["seasonNumber"]:
            for s in content_data["seasons"]:
                season: common.Season = common.Season()

                season.id = s["id"]
                season.title = s["title"]
                season.season_number = s["seasonNumber"]

                show.seasons.append(season)

        else:
            for s in reversed(content_data["seasons"]):
                season: common.Season = common.Season()

                season.id = s["id"]
                season.title = s["title"]
                season.season_number = s["seasonNumber"]

                show.seasons.append(season)



    def Season(self, season: common.Season) -> None:

        url: str = "https://www.noovo.ca/space-graphql/apq/graphql"

        graphql_operation_name = "season"

        graphql_variables: dict[str, str | list[str] | None] = {
            "seasonId": season.id,
		    "authenticationState": "UNAUTH",
		    "language": "FRENCH",
		    "maturity": "ADULT",
		    "playbackLanguage": "FRENCH",
		    "subscriptions": [
		        "CANAL_D",
		        "CANAL_VIE",
		        "INVESTIGATION",
		        "NOOVO",
		        "Z"
		    ]
        }


        graphql_query = """
query season($seasonId: ID!, $subscriptions: [Subscription]!, $maturity: Maturity!, $language: Language!, $authenticationState: AuthenticationState!, $playbackLanguage: PlaybackLanguage!) @uaContext(subscriptions: $subscriptions, maturity: $maturity, language: $language, authenticationState: $authenticationState, playbackLanguage: $playbackLanguage) {
    axisSeason(id: $seasonId) {
        episodes {
            axisId
            title
            duration
            agvotCode
            description
            summary
            episodeNumber
            seasonNumber
            originalSpokenLanguage
            contentType
            broadcastDate
            startsOn
            authConstraints {
                authRequired
                packageName
                language
            }
            axisPlaybackLanguages {
                destinationCode
                language
                playbackIndicators
            }
            playbackMetadata {
                indicator
                languages {
                    languageCode
                }
            }
        }
    }
}
"""

        data: dict[str, str | dict[str, str | list[str] | None]] = {
            "operationName": graphql_operation_name,
            "query": graphql_query,
            "variables": graphql_variables,
        }

        headers: dict[str, str] = {
            "content-type": "application/json"
        }

        r: requests.Response = requests.post(url, headers=headers, data=json.dumps(data))

        resp = r.json()
        with open("season.json", "wt") as f:
                f.write(json.dumps(resp))
        
        episodes = resp["data"]["axisSeason"]["episodes"]

        season.episodes = []

        for e in episodes:
            episode = common.Episode()

            episode.title = e["title"]
            episode.media_id = e["axisId"]
            episode.episode_number = e["episodeNumber"]
            episode.description = e["description"]
            # Need to verify content type so it matches other services
            episode.content_type = e["contentType"]
            # Don't know if that works, never seen a broadcastDate that's not null
            if e["broadcastDate"]:
                #episode.release_year = e["broadcastDate"][:4]
                pass
            
            episode.server_code = e["axisPlaybackLanguages"][0]["destinationCode"]
            episode.language = e["axisPlaybackLanguages"][0]["language"]
            
            if e["authConstraints"][0]["authRequired"]:
                episode.availability = "Premium"
            else:
                episode.availability = "Free"
            
            episode.available_audios = []
            episode.available_subtitles = []
            
            for media in e["playbackMetadata"]:
                match media["indicator"]:
                    case "DESCRIBED_VIDEO":
                        episode.audio_description_available = True
                        for language in media["languages"]:
                            audio = Audio()
                            audio.audio_description = True
                            audio.default = False
                            audio.language = language["languageCode"]
                            episode.available_audios.append(audio)
                            # NEED TO ADD LANGUAGE CHOICE OPTION
                    
                    case "AUDIO":
                        for language in media["languages"]:
                            audio = Audio()
                            audio.audio_description = False
                            audio.default = True
                            audio.language = language["languageCode"]
                            episode.available_audios.append(audio)
        
                    case "CLOSED_CAPTIONS":
                        episode.subtitles_available = True
                        for language in media["languages"]:
                            subtitle = Subtitle()
                            subtitle.language = language["languageCode"]
                            episode.available_subtitles.append(subtitle)
            
            season.episodes.append(episode)
        

    def Episode(self, episode: common.Episode) -> None:

        url: str = "https://www.noovo.ca/space-graphql/apq/graphql"

        graphql_operation_name = "axisContent"

        graphql_variables: dict[str, str | list[str] | None] = {
		    "authenticationState": "UNAUTH",
		    "id": f"contentid/axis-content-{episode.media_id}",
		    "language": "FRENCH",
		    "maturity": "ADULT",
		    "playbackLanguage": "FRENCH",
		    "subscriptions": [
		    	"CANAL_D",
		    	"CANAL_VIE",
		    	"INVESTIGATION",
		    	"NOOVO",
		    	"Z"
		    ]
        }




        graphql_query = """
query axisContent($id: ID!, $subscriptions: [Subscription]!, $maturity: Maturity!, $language: Language!, $authenticationState: AuthenticationState!, $playbackLanguage: PlaybackLanguage!) @uaContext(subscriptions: $subscriptions, maturity: $maturity, language: $language, authenticationState: $authenticationState, playbackLanguage: $playbackLanguage) {
    axisContent(id: $id) {
        axisId
        title
        duration
        agvotCode
        description
        summary
        episodeNumber
        seasonNumber
        originalSpokenLanguage
        contentType
        broadcastDate
        startsOn
        axisMedia {
            heroBrandLogoId
            id
        }
        authConstraints {
            authRequired
            packageName
            language
        }
        axisPlaybackLanguages {
            destinationCode
            language
            playbackIndicators
        }
        playbackMetadata {
            indicator
            languages {
                languageCode
            }
        }
    }
}
"""

        data: dict[str, str | dict[str, str | list[str] | None]] = {
            "operationName": graphql_operation_name,
            "query": graphql_query,
            "variables": graphql_variables,
        }

        headers: dict[str, str] = {
            "content-type": "application/json"
        }

        r: requests.Response = requests.post(url, headers=headers, data=json.dumps(data))

        resp = r.json()
        with open("episode.json", "wt") as f:
            f.write(json.dumps(resp))
        
        axis_content = resp["data"]["axisContent"]

        episode.title = axis_content["title"]
        episode.media_id = axis_content["axisId"]
        episode.episode_number = axis_content["episodeNumber"]
        episode.description = axis_content["description"]
        # Need to verify content type so it matches other services
        episode.content_type = axis_content["contentType"]
        # Don't know if that works, never seen a broadcastDate that's not null
        if axis_content["broadcastDate"]:
            #episode.release_year = axis_content["broadcastDate"][:4]
            pass
            
        episode.server_code = axis_content["axisPlaybackLanguages"][0]["destinationCode"]
        episode.language = axis_content["axisPlaybackLanguages"][0]["language"]
            
        if axis_content["authConstraints"][0]["authRequired"]:
            episode.availability = "Premium"
        else:
            episode.availability = "Free"
            
        episode.available_audios = []
        episode.available_subtitles = []
            
        for media in axis_content["playbackMetadata"]:
            match media["indicator"]:
                case "DESCRIBED_VIDEO":
                    episode.audio_description_available = True
                    for language in media["languages"]:
                        audio = Audio()
                        audio.audio_description = True
                        audio.default = False
                        audio.language = language["languageCode"]
                        episode.available_audios.append(audio)
                        # NEED TO ADD LANGUAGE CHOICE OPTION
                    
                case "AUDIO":
                    for language in media["languages"]:
                        audio = Audio()
                        audio.audio_description = False
                        audio.default = True
                        audio.language = language["languageCode"]
                        episode.available_audios.append(audio)
        
                case "CLOSED_CAPTIONS":
                    episode.subtitles_available = True
                    for language in media["languages"]:
                        subtitle = Subtitle()
                        subtitle.language = language["languageCode"]
                        episode.available_subtitles.append(subtitle)

        url: str = f"https://capi.9c9media.com/destinations/{episode.server_code}/platforms/desktop/contents/{episode.media_id}?$lang=fr&$include=[Desc,ContentPackages,Authentication,Season,Owner]"

        r: requests.Response = requests.get(url)

        resp = r.json()
        with open("episode.json", "wt") as f:
            f.write(json.dumps(resp))


        episode.title = resp["Name"]
        episode.description = resp["Desc"]
        episode.content_type = resp["Type"]
        
