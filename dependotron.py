"""
Depend-o-tron
Tool for finding dependencies of maven artifacts, using Python, SVN, Maven, MySQL, graphviz...
"""
from optparse import OptionParser
from database import Database
from pomProcessor import PomProcessor
from pomanalyser import PomAnalyser
from pomfetcherfolder import PomFetcherFolder
from pomfoundsubject import PomFoundSubject

__version__ = "0.0"

class Main:

    def __init__(self, path):
        self._starting_path = path
        self._max_items = 10
        self._pom_processor = None
        self._pom_found_subject = None

    def go(self):
        self._create_objects()
        self._pom_found_subject.register_observer(self._pom_processor)
        self._pom_processor.process()

    def _create_objects(self):
        self._pom_found_subject = PomFoundSubject()

        pom_fetcher = PomFetcherFolder(self._starting_path, self._max_items, self._pom_found_subject)
        # TODO switch pom_fetcher based on whether path is an svn or file path
        #pom_fetcher = PomFetcherSvn(self._starting_path, self._max_items, self._pom_found_subject)

        pom_analyser = PomAnalyser()
        database = Database()

        self._pom_processor = PomProcessor(pom_fetcher, pom_analyser, database)


# If run as a program then handle parameters and run
if __name__ == "__main__":
    print "This is Depend-O-Tron (version " + __version__ + ")"
    parser = OptionParser()
    parser.add_option("--svnRoot",
                        help = "The path to the initial SVN URL from which to start mapping dependencies.")

    main = None

    (options, args) = parser.parse_args()
    svn_root = options.svnRoot

    if svn_root:
        print "Starting crawling from: " + svn_root
        main = Main(svn_root)

    if (main):
        main.go()
    else:
        print "No svn or folder path specified. Sleeping zzzzzzzzzzzzzzz"