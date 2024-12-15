
import sys

from common.arguments import Arguments
from common.interface import Interface
from common.show import Show
from common.season import Season
from common.episode import Episode
from common.options import Options


from toutv_folder import Toutv


class Same:



    def TEST(self):

        argvs = sys.argv

        arguments = Arguments()

        options = Options()

        arguments.Parse(argvs, options)

        if arguments.method == "login":
            Toutv().Login(options)
        
        if arguments.method == "info":
            Toutv().Info(arguments.show_name)
        
        if arguments.method == "list":
            Toutv().List(arguments.show_name)
        
        if arguments.method == "search":
            Toutv().Search(arguments.show_name)
        
        if arguments.method == "download":
            Toutv().Download(arguments.show_name, options)





        



        #method(show, options)


if __name__ == "__main__":
    Same().TEST()
