"""
Depend-o-tron
Tool for finding dependencies of maven artifacts, using Python, SVN, Maven, MySQL, graphviz...
"""
import argparse
from pomanalyser import PomAnalyser
import database

__version__ = "0.0"


# Placeholder objects
class PomCrawler:
    def __init__(self, pomAnalyser, database):
        pass

    def crawl(self, svnRoot):
        """
        Start crawling the SVN system from [svnRoot].
        Uses [_pomAnalyser] to process each POM and writes the resulting information into [_database].
        """
        pass


class PomProcessor:
    def __init__(self, pomFetcher, pomAnalyser, database):
        pass

    def go(self):
        pass


# If run as a program then handle parameters and run
if __name__ == "__main__":
    print "This is Depend-O-Tron (version {0})".format(__version__)
    parser = argparse.ArgumentParser()
    parser.add_argument("--svnRoot",
                        help = "The path to the initial SVN URL from which to start mapping dependencies.")
    if parser.parse_args().svnRoot:
        print "Starting crawling from: {0}".format(parser.parse_args().svnRoot)

    database = database.Database()
    database.configure()

    pomAnalyser = PomAnalyser()

    pomFetcher = PomFetcherFolder()
    # pomFetcher = PomFetcherSvn()

    pomProcessor = PomProcessor(pomFetcher, pomAnalyser, database)
    pomProcessor.go()
