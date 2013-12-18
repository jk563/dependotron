"""
Depend-o-tron
Tool for finding dependencies of maven artifacts, using Python, SVN, Maven, MySQL, graphviz...
"""
import argparse

__version__ = "0.0"

#
# If run as a program then handle parameters and run
if __name__ == "__main__":
    print "This is Depend-O-Tron (version {0})".format(__version__)
    parser = argparse.ArgumentParser()
    parser.add_argument("--svnRoot",
                        help = "The path to the initial SVN URL from which to start mapping dependencies.")
    if parser.parse_args().svnRoot:
        print "Starting crawling from: {0}".format(parser.parse_args().svnRoot)
