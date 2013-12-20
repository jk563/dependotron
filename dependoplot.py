"""
Depend-o-tron graphviz plotter
"""
import unittest
import optparse

from artifactdependencyinfo import ArtifactInfo

try:
    from database import Database
except ImportError:
    pass


class Visualiser:
    def __init__(self, database):
        self.database = database
        self.preamble = []
        self.main = []
        self.postscript = []

    def build_graphviz_graph_for_artifact(self, artifact):
        if not self.database.doesArtifactExist(artifact.name, artifact.version):
            raise LookupError("Artifact " + str(artifact) + " is not known")
        self._plot_preamble()
        self._plot_downstream_dependencies(artifact)
        self._plot_upstream_dependencies(artifact)
        self._plot_postscript()
        graphviz_lines = self.preamble + self.main + self.postscript
        return graphviz_lines

    def _write(self, lines):
        for line in lines:
            print line

    def _plot_preamble(self):
        self.preamble.append("digraph G {")

    def _plot_postscript(self):
        self.postscript.append("}")

    def _plot_downstream_dependencies(self, artifact):
        print "Downstream dependencies for", artifact
        dependencyInfo = self.database.getDownstreamDependencies(artifact)
        (directCount, totalCount) = self._count_dependencies(dependencyInfo.dependencies)
        print "(direct = %d, total = %d)" % (directCount, totalCount)
        self.preamble.append(self._label_for(artifact))
        for dependency in dependencyInfo.dependencies:
            if dependency.direct_dependency:
                self.preamble.append(self._label_for(dependency))
                self.main.append(self._dependency_between(artifact.name, dependency.name))

    def _plot_upstream_dependencies(self, artifact):
        print "Upstream dependencies for", artifact
        dependencyInfo = self.database.getUpstreamDependencies(artifact)
        (directCount, totalCount) = self._count_dependencies(dependencyInfo.dependencies)
        print "(direct = %d, total = %d)" % (directCount, totalCount)
        self.preamble.append(self._label_for(artifact))
        for dependency in dependencyInfo.dependencies:
            if dependency.direct_dependency:
                self.preamble.append(self._label_for(dependency))
                self.main.append(self._dependency_between(dependency.name, artifact.name))

    def _dependency_between(self, source, destination):
        sanitised_source = self._sanitise(source)
        sanitised_destination = self._sanitise(destination)
        return "%s -> %s" % (sanitised_source, sanitised_destination)

    def _label_for(self, artifact_info):
        bits = artifact_info.name.split(":")
        nice_label = "\\n".join(bits)
        nice_label += "\\n" + artifact_info.version
        return "%s [label=\"%s\"];" % (self._sanitise(artifact_info.name), nice_label)

    def _sanitise(self, name):
        sanitised_name = name.replace(".", "_")
        sanitised_name = sanitised_name.replace(":", "_")
        sanitised_name = sanitised_name.replace("-", "_")
        return sanitised_name

    def _count_dependencies(self, dependencies):
        direct = 0
        for dependency in dependencies:
            if dependency.direct_dependency:
                direct += 1
        return (direct, len(dependencies))


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
    parser = optparse.OptionParser()
    # argparse.ArgumentParser("This is the graphviz plotting tool for Depend-O-Tron")
    parser.add_option("--artifactName",
                        help="The name of the artifact for which to show relationships")
    parser.add_option("--artifactVersion",
                        default="",
                        help="The version of the artifact for which to show relationships")
    parser.add_option("--steps",
                        default=1,
                        help="Maximum number of steps to show from the artifact")
    (options, args) = parser.parse_args()
    artifactName = options.artifactName
    artifactVersion = options.artifactVersion

    database = Database()
    artifactInfo = None

    artifactNameAndVersion = artifactName + ":" + artifactVersion
    if artifactName and database.doesArtifactExist(artifactName):
        visualiser = Visualiser(Database())
        artifacts = database.getArtifactInfo(artifactName, artifactVersion)
        for artifact in artifacts:
            print artifactNameAndVersion
            print artifact
            output_lines = visualiser.build_graphviz_graph_for_artifact(artifact)
            output_file = open(".temp/graph.dot", "w")
            for line in output_lines:
                print line
                output_file.write(line + "\n")
    else:
        print "Artifact (%s) not known." % (artifactNameAndVersion)
