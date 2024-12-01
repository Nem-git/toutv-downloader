


from common.audio import Audio
from common.interface import Interface
from common.options import Options
from common.season import Season
from common.show import Show

from common.download import Download
from common.video import Video
from common.pssh import Pssh
from common.name import Name

from toutv_folder.info import Info

class Whaat:
        
    def Download_Toutv(self, show: Show, options: Options) -> None:
        
        for season in show.seasons:
            for episode in season.episodes:

                episode = Info().Episodes(episode, options)
                
                # Need to fix how I choose videos, audio tracks and subtitles
                for video in episode.available_videos:
                    if options.resolution <= video.resolution_height:
                        episode.selected_video = video

                try:
                    episode.language = episode.selected_audios[0].language[:2].upper()
                except:
                    episode.language = "FR"
                
                for audio in episode.selected_audios:
                    if episode.language != audio.language:
                        episode.language = "MULTi"
                
                audio = Audio()
                audio.custom_string = ".main"
                audio.download_filters = 'role="main":'
                if (episode.language[:2]).upper() == "FR":
                    audio.language = "FR"
                    if show.country == "CA":
                        audio.language = "VFQ"

                elif episode.language[:2].upper() == "EN":
                    audio.language = "EN"

                else:
                    audio.language = "UND"
                
                episode.selected_audios.append(audio)
                
                #if options.audio_description:
                if True:
                    audio = Audio()
                    audio.custom_string = ".ad"
                    audio.download_filters = 'role="alternate":'

                    if episode.language[:2].upper() == "FR":
                        audio.language = "FR AD"
                        if show.country == "CA":
                            audio.language = "VFQ AD"

                    elif episode.language[:2].upper() == "EN":
                        audio.language = "EN AD"

                    else:
                        audio.language = "UND AD"
                    
                    episode.selected_audios.append(audio)

                #if options.subtitles:
                if 1 == 1:
                    episode.selected_subtitles = episode.available_subtitles

                episode.path = Name().Clean_Filename(show, season, episode, options)

                episode.clean_name = Name().Clean_Name(show, season, episode)

                # Token required to get mpd link
                options.license_headers = {"x-dt-auth-token": episode.request_token}

                episode.selected_video = Pssh().Get(episode, episode.selected_video, options)
                Download().Video(episode, options)
                
                for audio in episode.selected_audios:
                    Download().Audio(episode, audio, options)
                
                for subtitle in episode.selected_subtitles:
                    Download().Subtitles(episode, subtitle, options, {})
                
                Download().Merge(episode, options)