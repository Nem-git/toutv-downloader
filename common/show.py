from common.season import Season

class Show:
    id: str
    title: str = "No title available"
    description: str = "No description available"
    content_type: str = "Unknown Content Type"
    language: str = "Unknown Language"
    country: str = "Unknown Country"
    release_year: int = 0
    age_rating: str = "G"
    availability: str

    seasons: list[Season] = []