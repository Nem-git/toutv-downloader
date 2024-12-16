

from common.episode import Episode
from common.season import Season
from common.show import Show



class Interface:

    def Show_Search(self, shows: list[Show]) -> None:
        
        for show in shows:

            print("SHOW")
            print("-------------------------------------------------------")
            if show.title:
                print(f"Show title: {show.title}")
            if show.id:
                print(f"Show ID: {show.id}")
            print("-------------------------------------------------------")
            if show.content_type:
                print(f"Content type: {show.content_type}")
            print("-------------------------------------------------------")


    def Show_Info(self, show: Show) -> None:
        
        print("SHOW")
        print("-------------------------------------------------------")
        if show.title:
            print(f"Show title: {show.title}")
        if show.release_year:
            print(f"Release year: {show.release_year}")
        print("-------------------------------------------------------")
        if show.description:
            print(f"Description: {show.description}")
        print("-------------------------------------------------------")
        if show.country:
            print(f"Country: {show.country}")
        if show.language:
            print(f"Language: {show.language}")
        print("-------------------------------------------------------")
        if show.content_type:
            print(f"Content type: {show.content_type}")
        if show.age_rating:
            print(f"Content Rating: {show.age_rating}")
        print("-------------------------------------------------------")
        if show.seasons:
            print(f"{len(show.seasons)} seasons")
        
        episode_amount: int = 0
        for season in show.seasons:
            for _ in season.episodes:
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
        if season.title:
            print(f"Season title: {season.title}")
        if season.season_number:
            print(f"Season {season.season_number}")
        if season.release_year:
            print(f"Release year: {season.release_year}")
        print("-------------------------------------------------------")
        if season.description:
            print(f"Description: {season.description}")
        print("-------------------------------------------------------")
        if season.age_rating:
            print(f"Content Rating: {season.age_rating}")
        if season.availability:
            print(f"Content Availability: {season.availability}")
        print("-------------------------------------------------------")
        if season.episodes:
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
        if episode.title:
            print(f"Episode title: {episode.title}")
        if episode.episode_number:
            print(f"Episode {episode.episode_number}")
        if episode.release_year:
            print(f"Release year: {episode.release_year}")
        print("-------------------------------------------------------")
        if episode.description:
            print(f"Description: {episode.description}")
        print("-------------------------------------------------------")
        if episode.ad:
            print(f"Is an ad: {episode.ad}")
        if episode.subtitles_available:
            print(f"Subtitles available: {episode.subtitles_available}")
        if episode.audio_description_available:
            print(f"Audio Description Available: {episode.audio_description_available}")
        print("-------------------------------------------------------")
        if episode.drm_techs:
            print(f"DRM Available: {episode.drm_techs}")
        if episode.server_code:
            print(f"Server name: {episode.server_code}")
        print("-------------------------------------------------------")