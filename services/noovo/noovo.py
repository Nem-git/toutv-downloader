import common

#from services.noovo.download import Download
from services.noovo.info import Info
from services.noovo.login import Login
from services.noovo.search import Search


class Noovo:

    def Login(self, options: common.Options) -> None:
        Login().Login(options)
    
    def Search(self, show_name: str) -> list[common.Show]:
        shows: list[common.Show] = Search().Shows(show_name)
        common.Interface().Show_Search(shows)

        return shows
    
    def Info(self, show_name: str) -> common.Show:
        shows: list[common.Show] = Search().Shows(show_name)
        show: common.Show = shows[0]
        Info().Shows(show)
        common.Interface().Show_Info(show)

        return show

    def List(self, show_name: str) -> common.Show:
        shows: list[common.Show] = self.Search(show_name)
        show: common.Show = shows[0]
        Info().Shows(show)
        common.Interface().Show_List(show)

        return show

    def Download(self, show_name: str, options: common.Options) -> None:
        shows: list[common.Show] = Search().Shows(show_name)
        show: common.Show = shows[0]
        Info().Shows(show)
        Login().Login(options)

        options.headers["Authorization"] = options.authorization_token
        options.headers["x-claims-token"] = options.claims_token

        Download().Download(show, options)