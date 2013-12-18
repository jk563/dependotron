"""
Depend-o-tron
Tool for finding dependencies of maven artifacts, using Python, SVN, Maven, MySQL, graphviz...
"""
import argparse

__version__ = "0.0"


# Placeholder objects
class Database:
    def __init__(self):
        pass

    def configure(self):
        """
        Tests if the database is there, builds it if not. Maybe throws exception if wrong schema?
        Alternatively this could be done in the constructor
        """
        pass

    def add(self, dependencyEntry):
        """
        Add new information to the database. [dependencyEntry] might be a tuple of:
        (dependencyName, dependencyVersion, dependentName, dependentVersion)
        """
        pass

class PomCrawler:
    def __init__(self, pomAnalyser, database):
        pass

    def crawl(self, svnRoot):
        """
        Start crawling the SVN system from [svnRoot].
        Uses [_pomAnalyser] to process each POM and writes the resulting information into [_database].
        """
        pass

class PomAnalyser:
    def __init__(self):
        pass

    def analyse(self, pom):
        """
        Analyses the contents of [pom] and returns a list of tuples of depenencies.
        Uses maven to do the analysis.
        Q: can it take the contents of a POM or does it need to fetch it?
        """
        pass


# If run as a program then handle parameters and run
if __name__ == "__main__":
    print "This is Depend-O-Tron (version {0})".format(__version__)
    parser = argparse.ArgumentParser()
    parser.add_argument("--svnRoot",
                        help = "The path to the initial SVN URL from which to start mapping dependencies.")
    if parser.parse_args().svnRoot:
        print "Starting crawling from: {0}".format(parser.parse_args().svnRoot)

    database = Database()
    database.configure()

    pomAnalyser = PomAnalyser()

    pomCrawler = PomCrawler(pomAnalyser, database)
    pomCrawler.crawl(parser.parse_args().svnRoot)
