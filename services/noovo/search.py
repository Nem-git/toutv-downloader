
import requests
import json

from common.show import Show

class Search:

    def Shows(self, query: str) -> list[Show]:

        url: str = "https://www.noovo.ca/space-graphql/apq/graphql"

        graph_operation_name = "searchResults"

        graphql_variables = {
            "title": query,
            "pageSize": 100,
            "subscriptions": [
                "CANAL_D",
                "CANAL_VIE",
                "INVESTIGATION",
                "NOOVO",
                "Z"
            ],
            "maturity": "ADULT",
            "language": "FRENCH",
            "authenticationState": "UNAUTH",
            "playbackLanguage": "FRENCH"
        }

        graphql_query = """
query searchResults($title: String!, $pageSize: Int!, $page: Int = 0, $subscriptions: [Subscription]!, $maturity: Maturity!, $language: Language!, $authenticationState: AuthenticationState!, $playbackLanguage: PlaybackLanguage!) @uaContext(subscriptions: $subscriptions, maturity: $maturity, language: $language, authenticationState: $authenticationState, playbackLanguage: $playbackLanguage) {
    searchResults: searchMedia(titleMatches: $title, pageSize: $pageSize) {
        ... on Medias {
            page(page: $page) {
                items {
                    axisId
                    title
                    mediaType
                }
            }
        }
    }
}
"""

        data: dict[str, str | dict[str, str | int | list[str]]] = {
            "operationName": graph_operation_name,
            "query": graphql_query,
            "variables": graphql_variables,
        }
        
        r: requests.Response = requests.post(url, data=json.dumps(data))

        while not r.ok:
            r: requests.Response = requests.post(url, data=json.dumps(data))
        
        search_response = r.json()

        shows: list[Show] = []
        for result in search_response["data"]["searchResults"]["page"]["items"]:

            show = Show()
            show.id = result["axisId"]
            show.title = result["title"]

            # Types:
            # SERIES: Shows, comme Occupation double
            # SPECIAL: Emission speciale, comme genre /emissions/la-quete-de-khate, show d'humour ou documentaire
            # MOVIE: Film calisse

            show.content_type = result["mediaType"].capitalize()

            if show.content_type in ["Special", "Movie"]:
                show.content_type = "Movie"
            
            shows.append(show)

        return shows
