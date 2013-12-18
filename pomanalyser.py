"""
Takes the contents of a pom file and, using Maven, determines the dependencies.
Depends on:
    - Maven: to interface with its repository and determine dependencies
Does not depend on!
    - SVN: we get given the contents of the POM directly, regardless of where it came from
"""
import unittest
import tempfile
from subprocess import call


class ArtifactDependencyInfo:
    """
    Simple wrapper around the following directory.
    ((name, version), [(name, version, direct), ...)])
    """
    def __init__(self, artifactInfo, dependencies):
        self.artifactInfo = artifactInfo
        self.dependencies = dependencies


class PomAnalyser:
    def __init__(self):
        pass

    def analyse(self, pomContents, use_direct_only = True):
        """
        Analyses the contents of [pom] and returns a list of tuples of dependencies.
        Uses maven to do the analysis.
        Returns an ArtifactDependencyInfo
        """
        print "pomanalyser: hi! %d" % use_direct_only
        pomTemporaryPath = self._save_pom_contents_to_temporary_path(pomContents)
        self._do_some_maven_magic(pomTemporaryPath)
        return ArtifactDependencyInfo("", [])

    def _save_pom_contents_to_temporary_path(self, pomContents):
        temporaryPathAndFileName = tempfile.NamedTemporaryFile().name
        tempFile = open(temporaryPathAndFileName, "w")
        tempFile.writelines(pomContents)
        return temporaryPathAndFileName

    def _do_some_maven_magic(self, pomTemporaryPath):
        print ">>> _do_some_maven_magic called with", pomTemporaryPath
        call(["ls", "-l"])




# If run as a program then run unit tests
if __name__ == "__main__":
    pomFile = open("test/resources/simple_pom/pom.xml")
    pomContents = pomFile.readlines()
    analyser = PomAnalyser()

    dependencyInfo = analyser.analyse(pomContents)
    print dependencyInfo
