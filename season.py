from episode import Episode

class Season:
    id: str
    title: str
    description: str
    season_number: str
    release_year: int
    age_rating: str
    availability: str
    
    episodes: list[Episode]