from common.season import Season

class Show:
    id: str | None = None
    title: str | None = None
    description: str | None = None
    content_type: str | None = None
    language: str | None = None
    country: str | None = None
    release_year: int | None = None
    age_rating: str | None = None
    availability: str | None = None

    seasons: list[Season] = []