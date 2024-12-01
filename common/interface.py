

from common.episode import Episode
from common.season import Season
from common.show import Show



class Interface:

    # Shows Content Types: 
    # Show (Genre emission sans sens dans les saisons, vite-pas-vite)
    # Season (Genre Stat, emission ou il y a une histoire)
    # Collection (Regroupement de choses qui font du sens ensemble, genre collection/scene-comique)
    # Media (Un certain episode qui pour une raison est cherchable, Volleyball et « volley-splash », vite-pas-vite/s04e24)
    def Show_Search(self, shows: list[Show]) -> None:
        
        for show in shows:

            print("SHOW")
            print("-------------------------------------------------------")
            print(f"Show title: {show.title}")
            print(f"Show ID: {show.id}")
            print("-------------------------------------------------------")
            print(f"Content type: {show.content_type}")
            print("-------------------------------------------------------")


    def Show_Info(self, show: Show) -> None:
        
        print("SHOW")
        print("-------------------------------------------------------")
        print(f"Show title: {show.title}")
        print(f"Release year: {show.release_year}")
        print("-------------------------------------------------------")
        print(show.description)
        print("-------------------------------------------------------")
        print(f"Country: {show.country}")
        print(f"Language: {show.language}")
        print("-------------------------------------------------------")
        print(f"Content type: {show.content_type}")
        print(f"Content Rating: {show.age_rating}")
        print("-------------------------------------------------------")
        print(f"{len(show.seasons)} seasons")
        
        episode_amount: int = 0
        for season in show.seasons:
            for episode in season.episodes:
                episode_amount += 1
        
        print(f"{episode_amount} episodes")
        print("-------------------------------------------------------")
    

    def Show_List(self, show: Show) -> None:

        self.Show_Info(show)
        
        for season in show.seasons:
            for episode in season.episodes:
                print(f"S{season.season_number:02} E{episode.episode_number:02} | {show.title} | {season.title} | {episode.title}")
                print("-------------------------------------------------------")


    def Season_Info(self, season: Season) -> None:

        print("SEASON")
        print("-------------------------------------------------------")
        print(f"Season title: {season.title}")
        print(f"Season {season.season_number}")
        print(f"Release year: {season.release_year}")
        print("-------------------------------------------------------")
        print(season.description)
        print("-------------------------------------------------------")
        print(f"Content Rating: {season.age_rating}")
        print(f"Content Availability: {season.availability}")
        print("-------------------------------------------------------")
        print(f"{len(season.episodes)} episodes")
        print("-------------------------------------------------------")
    

    def Season_List(self, season: Season) -> None:

        self.Season_Info(season)

        for episode in season.episodes:
            print(f"S{season.season_number:02} E{episode.episode_number:02} | {season.title} | {episode.title}")
            print("-------------------------------------------------------")
    

    def Episode_Info(self, episode: Episode) -> None:
        # Episode Content types:
        # Episode (Normal media)
        # Trailer (Ad)
        print("EPISODE")
        print("-------------------------------------------------------")
        print(f"Episode title: {episode.title}")
        print(f"Episode {episode.episode_number}")
        print(f"Release year: {episode.release_year}")
        print("-------------------------------------------------------")
        print(episode.description)
        print("-------------------------------------------------------")
        print(f"Ad: {episode.ad}")
        print(f"Subtitles available: {episode.subtitles_available}")
        print(f"Audio Description Available: {episode.audio_description_available}")
        print("-------------------------------------------------------")
        print(f"DRM Available: {episode.drm_techs}")
        print(f"Server name: {episode.server_code}")
        print("-------------------------------------------------------")