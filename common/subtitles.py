import requests

from common.episode import Episode


class Subtitles:

    def Subtitles(self, episde: Episode) -> None:
        r = requests.get()