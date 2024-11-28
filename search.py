import requests

from show import Show

class Search:

    def Shows(self, query: str) -> list[Show]:
        url: str = f"https://services.radio-canada.ca/ott/catalog/v1/toutv/search?device=web&pageNumber=1&pageSize=999999999&term={query}"

        r: requests.Response = requests.get(url)

        while not r.ok:
            r: requests.Response = requests.get(url)
        
        search_response: dict[str, str] = r.json()

        shows: list[Show] = []
        for result in search_response["result"]:
            
            show = Show()
            show.id = result["url"]
            show.title = result["title"]
            show.content_type = result["type"]

            shows.append(show)
        
        return shows