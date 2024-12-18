
import json
import requests

import common
from common import season


class Info:

    def Show(self, show: common.Show) -> None:
        url: str = "https://www.noovo.ca/space-graphql/apq/graphql"

        graph_operation_name = "axisMedia"

        graphql_variables: dict[str, str | list[str] | None] = {
		    "authenticationState": "UNAUTH",
		    "axisMediaId": show.id,
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
            "operationName": graph_operation_name,
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

            
        print("WAIT")


    def Season(self, season: common.Season) -> None:

        url: str = "https://www.noovo.ca/space-graphql/apq/graphql"

        graph_operation_name = "season"

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
            id
            axisId
            title
            episodeNumber
            description
            summary
            duration
            seasonNumber
            contentType
            broadcastDate
            axisPlaybackLanguages {
                destinationCode
                language
                duration
                playbackIndicators
                partOfMultiLanguagePlayback
            }
            authConstraints {
                authRequired
                packageName
                language
                subscriptionName
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

fragment AuthConstraintsData on AuthConstraint {
    authRequired
    packageName
    endDate
    language
    startDate
    subscriptionName
}

fragment AxisPlaybackData on AxisPlayback {
    destinationCode
    language
    duration
    playbackIndicators
    partOfMultiLanguagePlayback
}
"""

        data: dict[str, str | dict[str, str | list[str] | None]] = {
            "operationName": graph_operation_name,
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

        
        
