"""
Depend-o-tron graphviz plotter
"""
import argparse
import unittest
from artifactdependencyinfo import ArtifactInfo

try:
    from database import Database
except ImportError:
    pass


class Visualiser:
    def __init__(self, database):
        self.database = database

    def plot_graph_for_artifact(self, artifact):
        if not self.database.doesArtifactExist(artifact):
            raise LookupError("Artifact " + artifact + " is not known")


##########################################################################################
# Tests and Mocking libraries

class MockDatabase:
    def __init__(self, known_artifacts):
        self.known_artifacts = known_artifacts

    def doesArtifactExist(self, name, version = None):
        return name in self.known_artifacts

    def getArtifactInfo(self, artifactName, artifactVersion=None):
        return [ArtifactInfo("name1", "version1"), ArtifactInfo("name2", "version2")]


class VisualiserTest(unittest.TestCase):
    def setUp(self):
        self.mock_database = MockDatabase(["foo"])
        self.visualiser = Visualiser(self.mock_database)

    def test_given_database_knows_artifact_when_plot_graph_then_does_not_throw_exception(self):
        self.visualiser.plot_graph_for_artifact("foo")

    def test_given_database_does_not_know_artifact_when_plot_graph_then_does_throw_exception(self):
        self.assertRaises(LookupError, self.visualiser.plot_graph_for_artifact, "bar")


# If run as a program then handle parameters and run
if __name__ == "__main__":
    parser = argparse.ArgumentParser("This is the graphviz plotting tool for Depend-O-Tron")
    parser.add_argument("artifact",
                        help="The artifact for which to show relationships")
    parser.add_argument("--steps",
                        default=1,
                        help="Maximum number of steps to show from the artifact")
    args = parser.parse_args()

    if args.artifact:
        visualiser = Visualiser(Database())
        visualiser.plot_graph_for_artifact(args.artifact)
