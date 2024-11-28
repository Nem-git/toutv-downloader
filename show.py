from season import Season

class Show:
    id: str
    title: str
    description: str
    content_type: str
    language: str
    country: str
    release_year: int
    availability: str

    seasons: list[Season]