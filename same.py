import sys

from common.download import Download
import tools

from common.show import Show
from common.season import Season
from common.episode import Episode
from toutv_folder import whaat
from toutv_folder.info import Info
from toutv_folder.login import Login
from common.options import Options
from toutv_folder.search import Search
from toutv_folder import Whaat



class Same:

    def TEST(self):
        options = Login().Login(Options())

        shows = Search().Shows("Bernard")

        show = Info().Shows(shows[0])

        Whaat().Download_Toutv(show, options)

Same().TEST()