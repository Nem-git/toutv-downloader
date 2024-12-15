from common.episode import Episode

class Season:
    id: str | None = None
    title: str | None = None
    description: str | None = None
    season_number: int | None = None
    release_year: int | None = None
    age_rating: str | None = None
    availability: str | None = None
    
    episodes: list[Episode] = []