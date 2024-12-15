

import subprocess

import requests
from common import options
from common.episode import Episode
from common.subtitle import Subtitle
from common.video import Video
from common.audio import Audio
from common.options import Options
from common.name import Name

class Download:

    def Merge(self, episode: Episode, options: Options) -> None:
        
        mkvmerge_command: list[str] = [
            "mkvmerge",
            "-o",
            f"{options.download_path}{episode.path}.mkv",
            "--title",
            episode.clean_name,
            "--default-language",
            episode.language,
            "--original-flag",
            "0",
            "--default-track-flag",
            "0",
            "--track-name",
            f"0:original {episode.selected_video.resolution_height}p",
            f"{options.download_path}{episode.path}.mp4"
        ]

        for audio in episode.selected_audios:

            command: list[str] = []

            if audio.audio_description:
                command.extend(["--visual-impaired-flag", "1"])
            
            if audio.default:
                command.extend(["--default-track-flag", "0"])
            
            else:
                command.extend(["--default-track-flag", "0:0"])

            command.extend([
                "--language", f'0:{audio.language}',
                "--track-name", f"0:{audio.name}",
                Name().Find_Filename(episode.path, ".m4a", options.download_path)[0]
            ])

            mkvmerge_command.extend(command)
            

        for subtitle in episode.selected_subtitles:
            if options.subtitles:
                mkvmerge_command.extend([
                    "--language", f'0:{subtitle.language}',
                    "--track-name", f"0:{subtitle.title.lower()} ",
                    Name().Find_Filename(episode.path, f".{subtitle.type.lower()}", options.download_path)[0]
                ])
        
        subprocess.run(mkvmerge_command)
        
        Name().Remove_Filename(episode.path, options.download_path, [".mp4", ".m4a", ".vtt", ".srt"])





    def Subtitles(self, episode: Episode, subtitle: Subtitle, options: Options, headers: dict[str, str]) -> None:
        subtitle_content: bytes = requests.get(subtitle.url, headers=headers).content

        with open(f"{episode.path}.{subtitle.type.lower()}", "wb") as f:
            f.write(subtitle_content)
    

    def Audio(self, episode: Episode, audio: Audio, options: Options) -> None:

        n_m3u8dl_re_command = [
            "n-m3u8dl-re",
            episode.url,
            "--decryption-engine",
            "FFMPEG",
            "-sa",
            f'{audio.download_filters}for=best',
            "--save-dir",
            options.download_path,
            "--save-name",
            f"{episode.path}{audio.custom_string}"
        ]

        # Need to add option for quiet
        subprocess.run(n_m3u8dl_re_command)


    def Video(self, episode: Episode, options: Options) -> None:

        n_m3u8dl_re_command = [
            "n-m3u8dl-re",
            episode.url,
            "--decryption-engine",
            "SHAKA_PACKAGER",
            "-sv",
            f"{episode.selected_video.download_filters}for=best",
            "--save-dir",
            options.download_path,
            "--save-name",
            f"{episode.path}{episode.selected_video.custom_string}.dirty"
        ]

        for key in episode.selected_video.decryption_keys:
            n_m3u8dl_re_command.append("--key")
            n_m3u8dl_re_command.append(key)
        
        # Need to add option for quiet
        subprocess.run(n_m3u8dl_re_command)

        # Remove phantom subtitles
        ffmpeg_command: list[str] = [
            "ffmpeg",
            "-i",
            f"{options.download_path}{episode.path}.dirty.mp4",
            "-map",
            "0",
            "-codec",
            "copy",
            "-y"
        ]

        if episode.selected_video.filter_unit != []:
            ffmpeg_command.extend(episode.selected_video.filter_unit)

        ffmpeg_command.append(f"{options.download_path}{episode.path}.mp4")

        # Need to add option for quiet
        subprocess.run(ffmpeg_command)



