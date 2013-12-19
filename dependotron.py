"""
Depend-o-tron
Tool for finding dependencies of maven artifacts, using Python, SVN, Maven, MySQL, graphviz...
"""
from optparse import OptionParser
from database import Database
from pomProcessor import PomProcessor
from pomanalyser import PomAnalyser
from pomfetcherfolder import PomFetcherFolder
from pomfetchersvn import PomFetcherSvn
from pomfoundsubject import PomFoundSubject

__version__ = "0.0"

class Main:

    def __init__(self, path, svn_or_folder):
        self._starting_path = path
        self._max_items = 10
        self._pom_processor = None
        self._pom_found_subject = None
        self._svn_or_folder = svn_or_folder

    def go(self):
        self._create_objects()
        self._pom_found_subject.register_observer(self._pom_processor)
        self._pom_processor.process()

    def _create_objects(self):
        self._pom_found_subject = PomFoundSubject()

        if self._svn_or_folder == "FOLDER":
            pom_fetcher = PomFetcherFolder(self._starting_path, self._max_items, self._pom_found_subject)
        elif self._svn_or_folder == "SVN":
            pom_fetcher = PomFetcherSvn(self._starting_path, self._max_items, self._pom_found_subject)

        pom_analyser = PomAnalyser()
        database = Database()

        self._pom_processor = PomProcessor(pom_fetcher, pom_analyser, database)


# If run as a program then handle parameters and run
if __name__ == "__main__":
    print "This is Depend-O-Tron (version " + __version__ + ")"
    parser = OptionParser()
    parser.add_option("--svnRoot", help = "The path to the initial SVN URL from which to start mapping dependencies.")
    parser.add_option("--xmlFolder", help = "The path to a folder containing POMs-as-XML-files from which to start mapping dependencies")

    main = None

    (options, args) = parser.parse_args()
    svn_root = options.svnRoot
    xml_folder = options.xmlFolder

    if svn_root:
        print "Starting crawling from: " + svn_root
        main = Main(svn_root, "SVN")
    elif xml_folder:
        print "Processing XML files from: " + xml_folder
        main = Main(xml_folder, "FOLDER")

    if main:
        main.go()
    else:
        print "No svn or folder path specified. Sleeping zzzzzzzzzzzzzzz"