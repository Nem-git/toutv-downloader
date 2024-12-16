
import common

#import pycountry

import common.language
from services.toutv.info import Info

class Download:
        
    def Download(self, show: common.Show, options: common.Options) -> None:
        
        for season in show.seasons:
            if season.season_number > options.end_season:
                break
            if options.latest_episode and season != show.seasons[-1]:
                continue
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

                Info().Episodes(episode, options)

                # ONLY APPLIES TO TOUTV
                #-------------------------------------------------------------------------------
                
                # Need to fix how I choose videos, audio tracks and subtitles
                for video in episode.available_videos:
                    
                    if options.resolution:
                        video.download_filters += f"res='{options.resolution}*':"
                    if options.video_codec:
                        video.download_filters += f"codecs='{options.video_codec}'"
                    if not episode.selected_video:
                        episode.selected_video = video

                    if options.resolution <= video.resolution_height:
                        episode.selected_video = video

                episode.selected_video.codec = "avc"
                episode.selected_video.filter_unit= ["-bsf:v", "'filter_units=remove_types=6'"]
                
                #for audio in episode.selected_audios:
                #    NEED TO FIX HAVING MULTIPLE LANGUAGES
                #    episode.language = common.Language().Fix(audio, show.country)
                
                audio = common.Audio()
                audio.custom_string = ".main"
                audio.download_filters = 'role="main":'
                audio.default = True
                audio.audio_description = False
                audio.language = show.language
                episode.language = common.Language().Fix(audio, show.country)

                # That's a fucking guess :D
                if episode.language == "und-CA" or episode.language == "fr-CA":
                    episode.language = "fr-CA"
                    audio.name = "VFQ"
                
                audio.language = episode.language
                
                episode.selected_audios.append(audio)
                
                if options.audio_description:
                    audio = common.Audio()
                    audio.custom_string = ".ad"
                    audio.download_filters = 'role="alternate":'
                    audio.default = False
                    audio.audio_description = True

                    audio.language = episode.selected_audios[0].language
                    audio.name = f"{episode.selected_audios[0].name} AD"
                    
                    episode.selected_audios.append(audio)

                if options.subtitles:
                    episode.selected_subtitles = episode.available_subtitles

                episode.path = common.Name().Clean_Filename(show, season, episode, options)

                # ONLY TOUTV
                episode.path = episode.path.replace("fr-CA", "VFQ")

                common.Name().Clean_Name(show, season, episode)

                # Token required to get mpd link
                options.license_headers = {"x-dt-auth-token": episode.request_token}

                episode.selected_video = common.Pssh().Get(episode, episode.selected_video, options)
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