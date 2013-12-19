"""
Depend-o-tron
Tool for finding dependencies of maven artifacts, using Python, SVN, Maven, MySQL, graphviz...
"""
import argparse
from database import Database
from pomProcessor import PomProcessor
from pomanalyser import PomAnalyser
from pomfetcherfolder import PomFetcherFolder
from pomfoundsubject import PomFoundSubject

__version__ = "0.0"

class Main:

    def __init__(self, path):
        self._starting_path = path
        self._pom_processor
        self._pom_found_subject

    def go(self):
        self._create_objects()
        self._pom_found_subject.register_observer(self._pom_processor)
        self._pom_processor.process()

    def _create_objects(self):
        self._pom_found_subject = PomFoundSubject()

        pom_fetcher = PomFetcherFolder(self._starting_path, self.max_items, self._pom_found_subject)
        # TODO switch pom_fetcher based on whether path is an svn or file path
        #pom_fetcher = PomFetcherSvn(self._starting_path, self.max_items, self._pom_found_subject)

        pom_analyser = PomAnalyser()
        database = Database()

        self._pom_processor = PomProcessor(pom_fetcher, pom_analyser, database)


# If run as a program then handle parameters and run
if __name__ == "__main__":
    print "This is Depend-O-Tron (version {0})".format(__version__)
    parser = argparse.ArgumentParser()
    parser.add_argument("--svnRoot",
                        help = "The path to the initial SVN URL from which to start mapping dependencies.")
    if parser.parse_args().svnRoot:
        print "Starting crawling from: {0}".format(parser.parse_args().svnRoot)

    main = Main(parser.parse_args().svnRoot)
    main.go()