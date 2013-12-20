"""
Depend-o-tron
Tool for finding dependencies of maven artifacts, using Python, SVN, Maven, MySQL, graphviz...
"""
from optparse import OptionParser
from logger import Logger
from database import Database
from pomProcessor import PomProcessor
from pomanalyser import PomAnalyser
from pomfetcherfolder import PomFetcherFolder
from pomfetchersvn import PomFetcherSvn
from pomfoundsubject import PomFoundSubject
from svnopener import SvnOpener

__version__ = "0.0"

class Main:

    def __init__(self, path, svn_or_folder, cert_file):
        self._starting_path = path
        self._max_items = 10
        self._pom_processor = None
        self._pom_found_subject = None
        self._pom_fetcher = None
        self._svn_or_folder = svn_or_folder
        self._cert_file = cert_file

    def go(self):
        self._create_objects()
        self._pom_found_subject.register_observer(self._pom_processor)
        self._pom_fetcher.fetch()

    def _create_objects(self):
        self._pom_found_subject = PomFoundSubject()
        logger = Logger()

        if self._svn_or_folder == "FOLDER":
            self._pom_fetcher = PomFetcherFolder(self._starting_path, self._max_items, self._pom_found_subject)
        elif self._svn_or_folder == "SVN":
            if self._cert_file == None:
                raise Exception("A cert file is required. Please re-run with the --certFile option")
            opener = SvnOpener.getOpener(self._cert_file, self._cert_file)
            self._pom_fetcher = PomFetcherSvn(opener, self._starting_path, self._max_items, self._pom_found_subject, logger)

        pom_analyser = PomAnalyser()
        database = Database()
        database.configure()

        self._pom_processor = PomProcessor(pom_analyser, database, logger)


# If run as a program then handle parameters and run
if __name__ == "__main__":
    print "This is Depend-O-Tron (version " + __version__ + ")"
    parser = OptionParser()
    parser.add_option("--svnRoot", help = "The path to the initial SVN URL from which to start mapping dependencies.")
    parser.add_option("--certFile", help = "The path to your developer .pem file, required for svn access")
    parser.add_option("--xmlFolder", help = "The path to a folder containing POMs-as-XML-files from which to start mapping dependencies")

    main = None

    (options, args) = parser.parse_args()
    svn_root = options.svnRoot
    xml_folder = options.xmlFolder
    cert_file = options.certFile

    if svn_root:
        print "Starting crawling from: " + svn_root
        main = Main(svn_root, "SVN", cert_file)
    elif xml_folder:
        print "Processing XML files from: " + xml_folder
        main = Main(xml_folder, "FOLDER", None)

    try:
        if main:
            main.go()
        else:
            print "No svn or folder path specified. Sleeping zzzzzzzzzzzzzzz"
    except Exception, e:
        print(e)
