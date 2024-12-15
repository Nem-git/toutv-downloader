

import common

from common.download import Download
from common.video import Video
from common.pssh import Pssh
from common.name import Name

import toutv_folder
import toutv_folder.search



class Toutv:


    def Login(self, options: common.Options) -> common.Options:
        options = toutv_folder.Login().Login(options)

        return options
    
    def Search(self, show_name: str) -> list[common.Show]:
        shows: list[common.Show] = toutv_folder.Search().Shows(show_name)
        common.Interface().Show_Search(shows)

        return shows
    
    def Info(self, show_name: str) -> common.Show:
        shows: list[common.Show] = toutv_folder.Search().Shows(show_name)
        show: common.Show = toutv_folder.Info().Shows(shows[0])
        common.Interface().Show_Info(show)

        return show

    def List(self, show_name: str) -> common.Show:
        shows: list[common.Show] = self.Search(show_name)
        show: common.Show = toutv_folder.Info().Shows(shows[0])
        common.Interface().Show_List(show)

        return show

    def Download(self, show_name: str, options: common.Options) -> None:
        shows: list[common.Show] = toutv_folder.Search().Shows(show_name)
        show: common.Show = toutv_folder.Info().Shows(shows[0])
        options = toutv_folder.Login().Login(options)

        options.headers["Authorization"] = options.authorization_token
        options.headers["x-claims-token"] = options.claims_token

        toutv_folder.Download().Download(show, options)

        


