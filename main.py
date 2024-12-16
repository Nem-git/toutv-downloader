
import sys

import common

from services.toutv import Toutv
#from services.crave import Crave
from services.noovo import Noovo


class Main:

    streaming_service_class = None

    def Main(self, arguments: common.Arguments, options: common.Options) -> None:

        if arguments.method == "login":
            self.streaming_service_class.Login(options)
        
        if arguments.method == "info":
            self.streaming_service_class.Info(arguments.show_name)
        
        if arguments.method == "list":
            self.streaming_service_class.List(arguments.show_name)
        
        if arguments.method == "search":
            self.streaming_service_class.Search(arguments.show_name)
        
        if arguments.method == "download":
            self.streaming_service_class.Download(arguments.show_name, options)


if __name__ == "__main__":

    arguments = common.Arguments()
    options = common.Options()
    main = Main()

    arguments.Parse(sys.argv, options)

    match arguments.streaming_servie:

        case "toutv":
            main.streaming_service_class = Toutv()
        
        case "crave":
            main.streaming_service_class = Crave()
        
        case "noovo":
            main.streaming_service_class = Noovo()

    main.Main(arguments, options)

