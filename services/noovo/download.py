
import common

#import pycountry

import common.language
from common.video import Video
from services.noovo.info import Info

class Download:
        
    def Download(self, show: common.Show, options: common.Options) -> None:
        
        for season in show.seasons:
            if season.season_number > options.end_season:
                break
            if options.latest_episode and season != show.seasons[-1]:
                continue
            Info().Season(season)
            for episode in season.episodes:

                if season.season_number == options.end_season and episode.episode_number > options.end_episode:
                    break

                if season.season_number == options.start_season and episode.episode_number < options.start_episode:
                    continue

                if options.latest_episode and episode != season.episodes[-1]:
                    continue
                
                # FUCK TRAILERS
                if episode.ad:
                    continue

                Info().Episode(episode)

                # ONLY APPLIES TO NOOVO
                #-------------------------------------------------------------------------------
                episode.selected_video = Video()

                # Need to fix how I choose videos, audio tracks and subtitles
                episode.selected_video.download_filters = ""
                    
                if options.resolution:
                    episode.selected_video.download_filters += f"res='{options.resolution}*':"
                if options.video_codec:
                    episode.selected_video.download_filters += f"codecs='{options.video_codec}'"

                episode.selected_video.codec = "avc"
                episode.selected_video.filter_unit = []
                episode.selected_video.filter_unit.append("-bsf:v")
                episode.selected_video.filter_unit.append("'filter_units=remove_types=6'")


                
                #for audio in episode.selected_audios:
                #    NEED TO FIX HAVING MULTIPLE LANGUAGES
                #    episode.language = common.Language().Fix(audio, show.country)

                episode.selected_audios = []

                for audio in episode.available_audios:
                    # That's a fucking guess :D
                    if episode.language == "und-CA" or episode.language == "fr-CA":
                        episode.language = "fr-CA"
                        audio.name = "VFQ"
                    
                    if audio.audio_description:
                        audio.name += " AD"
                    
                    # If you chose to have audio description OR it's the main audio, which is needed
                    if options.audio_description or audio.default:
                        episode.selected_audios.append(audio)
                    
                    
                    episode.language = common.Language().Fix(audio, show.country)

                if options.subtitles:
                    episode.selected_subtitles = episode.available_subtitles

                episode.path = common.Name().Clean_Filename(show, season, episode, options)

                # ONLY TOUTV
                episode.path = episode.path.replace("fr-CA", "VFQ")

                common.Name().Clean_Name(show, season, episode)

                common.Pssh().Get(episode, episode.selected_video, options)
                common.Download().Video(episode, options)
                
                for audio in episode.selected_audios:
                    common.Download().Audio(episode, audio, options)
                
                for subtitle in episode.selected_subtitles:
                    if not subtitle.title:
                        subtitle.title = episode.selected_audios[0].name
                    if not subtitle.language:
                        subtitle.language = episode.selected_audios[0].language
                    common.Download().Subtitles(episode, subtitle, options, {})
                
                common.Download().Merge(episode, options)
            
                #-------------------------------------------------------------------------------