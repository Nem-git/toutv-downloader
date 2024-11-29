

from common.episode import Episode
from common.season import Season
from common.show import Show



class Interface:

    def Show_Search(self, shows: list[Show]) -> None:
        
        for show in shows:
            print(show.title)
            print(show.id)
            print("-------------------------------------------------------")
            print(show.content_type)
            print("-------------------------------------------------------")


    def Show_Info(self, show: Show) -> None:
        
        print(show.title)
        print(show.release_year)
        print("-------------------------------------------------------")
        print(show.description)
        print("-------------------------------------------------------")
        print(show.country)
        print(show.language)
        print("-------------------------------------------------------")
        print(show.content_type)
        print(show.age_rating)
        print("-------------------------------------------------------")
        print(f"{len(show.seasons)} seasons")
        
        episode_amount: int
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

        print(season.title)
        print(season.season_number)
        print(season.release_year)
        print("-------------------------------------------------------")
        print(season.description)
        print("-------------------------------------------------------")
        print(season.age_rating)
        print(season.availability)
        print("-------------------------------------------------------")
        print(f"{len(season.episodes)} episodes")
        print("-------------------------------------------------------")
    

    def Season_List(self, season: Season) -> None:

        self.Season_Info(season)

        for episode in season.episodes:
            print(f"S{season.season_number:02} E{episode.episode_number:02} | {season.title} | {episode.title}")
            print("-------------------------------------------------------")
    

    def Episode_Info(self, episode: Episode) -> None:

        print(episode.title)
        print(episode.episode_number)
        print(episode.release_year)
        print("-------------------------------------------------------")
        print(episode.description)
        print("-------------------------------------------------------")
        print(f"Ad: {episode.ad}")
        print(f"Subtitles available: {episode.subtitles_available}")
        print(f"Audio Description Available: {episode.audio_description_available}")
        print("-------------------------------------------------------")
        print(episode.drm_techs)
        print(episode.server_code)
        print("-------------------------------------------------------")