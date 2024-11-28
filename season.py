from episode import Episode

class Season:
    id: str
    title: str
    description: str
    season_number: str
    availability: str
    
    episodes: list[Episode]