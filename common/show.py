from common.season import Season

class Show:
    id: str = ""
    title: str = ""
    description: str = ""
    content_type: str = ""
    language: str = ""
    country: str = ""
    release_year: int
    age_rating: str = ""
    availability: str = ""

    seasons: list[Season] = []