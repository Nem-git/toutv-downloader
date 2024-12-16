import requests

from common.show import Show

class Search:

    def Shows(self, query: str) -> list[Show]:
        url: str = f"https://services.radio-canada.ca/ott/catalog/v1/toutv/search?device=web&pageNumber=1&pageSize=999999999&term={query}"

        r: requests.Response = requests.get(url)

        while not r.ok:
            r: requests.Response = requests.get(url)
        
        search_response: dict[str, list[dict[str, str]]] = r.json()

        shows: list[Show] = []
        for result in search_response["result"]:
            
            show = Show()
            show.id = result["url"]
            show.title = result["title"]

            # TOUTV Shows Content Types: 
            # Show (Genre emission sans sens dans les saisons, vite-pas-vite)
            # Season (Genre Stat, emission ou il y a une histoire)
            # Collection (Regroupement de choses qui font du sens ensemble, genre collection/scene-comique)
            # Media (Un certain episode qui pour une raison est cherchable, Volleyball et « volley-splash », vite-pas-vite/s04e24)

            show.content_type = result["type"]

            if show.content_type == "Season":
                show.content_type = "Series"

            if show.content_type in ["Show", "Season"]:
            
                shows.append(show)
        
        return shows