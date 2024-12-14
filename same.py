
import sys

from common.show import Show
from common.season import Season
from common.episode import Episode
from toutv import info
from toutv_folder.info import Info
from toutv_folder.login import Login
from common.options import Options
from toutv_folder.search import Search
from toutv_folder import Whaat
from common.arguments import Arguments



class Same:

    def TEST(self):
        options = Login().Login(Options())

        argvs = sys.argv

        arguments = Arguments()

        arguments.Parse(argvs, options)

        shows = Search().Shows(arguments.show_name)

        show = Info().Shows(shows[0])

        streaming_service: Whaat
        method = ""

        if arguments.streaming_servie == "toutv":
            if arguments.method == "info":
                method = Info().Shows
        



        method(show, options)

Same().TEST()