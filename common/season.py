from common.episode import Episode

class Season:
    id: str
    title: str = "No title available"
    description: str = "No description available"
    season_number: int = 0
    release_year: int = 0
    age_rating: str = "G"
    availability: str
    
    episodes: list[Episode] = []