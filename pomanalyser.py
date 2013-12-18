"""
Takes the contents of a pom file and, using Maven, determines the dependencies.
Depends on:
    - Maven: to interface with its repository and determine dependencies
Does not depend on!
    - SVN: we get given the contents of the POM directly, regardless of where it came from
"""
import unittest


class PomAnalyser:
    def __init__(self):
        pass

    def analyse(self, pomContents, use_direct_only = True):
        """
        Analyses the contents of [pom] and returns a list of tuples of dependencies.
        Uses maven to do the analysis.
        Q: can it take the contents of a POM or does it need to fetch it?
        """
        print "pomanalyser: hi! %d" % use_direct_only


# If run as a program then run unit tests
if __name__ == "__main__":
    pomFile = open("test/resources/simple_pom/pom.xml")
    pomContents = pomFile.readlines()
    analyser = PomAnalyser()
    analyser.analyse(pomContents)
