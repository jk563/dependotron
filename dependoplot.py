"""
Depend-o-tron graphviz plotter
"""
import argparse
import unittest
import pprint

from artifactdependencyinfo import ArtifactInfo

try:
    from database import Database
except ImportError:
    pass


class Visualiser:
    def __init__(self, database):
        self.database = database

    def plot_graph_for_artifact(self, artifact):
        if not self.database.doesArtifactExist(artifact.name, artifact.version):
            raise LookupError("Artifact " + str(artifact) + " is not known")
        self._plot_downstream_dependencies(artifact)
        self._plot_upstream_dependencies(artifact)

    def _plot_downstream_dependencies(self, artifact):
        print "Downstream dependencies for", artifact
        dependencyInfo = self.database.getDownstreamDependencies(artifact)
        for dependency in dependencyInfo.dependencies:
            print dependency

    def _plot_upstream_dependencies(self, artifact):
        print "Upstream dependencies for", artifact
        dependencyInfo = self.database.getUpstreamDependencies(artifact)
        for dependency in dependencyInfo.dependencies:
            print dependency


##########################################################################################
# Tests and Mocking libraries

class MockDatabase:
    def __init__(self, known_artifacts):
        self.known_artifacts = known_artifacts

    def doesArtifactExist(self, name, version = None):
        return name in self.known_artifacts

    def getArtifactInfo(self, artifactName, artifactVersion=None):
        return [ArtifactInfo("name1", "version1"), ArtifactInfo("name2", "version2")]

    def getDownstreamDependencies(self, artifactInfo):
        pass

    def getUpstreamDependencies(self, artifactInfo):
        pass


class VisualiserTest(unittest.TestCase):
    def setUp(self):
        self.mock_database = MockDatabase(["foo"])
        self.visualiser = Visualiser(self.mock_database)

    def test_given_database_knows_artifact_when_plot_graph_then_does_not_throw_exception(self):
        self.visualiser.plot_graph_for_artifact("foo")

    def test_given_database_does_not_know_artifact_when_plot_graph_then_does_throw_exception(self):
        self.assertRaises(LookupError, self.visualiser.plot_graph_for_artifact, "bar")

    # def test_given_database_knows_artifact_then_when_plot_graph_then_


# If run as a program then handle parameters and run
if __name__ == "__main__":
    parser = argparse.ArgumentParser("This is the graphviz plotting tool for Depend-O-Tron")
    parser.add_argument("artifactName",
                        help="The name of the artifact for which to show relationships")
    parser.add_argument("--artifactVersion",
                        default="",
                        help="The version of the artifact for which to show relationships")
    parser.add_argument("--steps",
                        default=1,
                        help="Maximum number of steps to show from the artifact")
    args = parser.parse_args()
    database = Database()
    artifactInfo = None

    artifactNameAndVersion = args.artifactName + ":" + args.artifactVersion
    if args.artifactName and database.doesArtifactExist(args.artifactName):
        visualiser = Visualiser(Database())
        artifacts = database.getArtifactInfo(args.artifactName, args.artifactVersion)
        for artifact in artifacts:
            print artifactNameAndVersion
            print artifact
            visualiser.plot_graph_for_artifact(artifact)
    else:
        print "Artifact (%s) not known." % (artifactNameAndVersion)
