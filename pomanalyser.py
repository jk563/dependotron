"""
Takes the contents of a pom file and, using Maven, determines the dependencies.
Depends on:
    - Maven: to interface with its repository and determine dependencies
Does not depend on!
    - SVN: we get given the contents of the POM directly, regardless of where it came from
"""
import unittest
import os
import re

from artifactdependencyinfo import ArtifactDependencyInfo
from artifactdependencyinfo import ArtifactInfo


class PomAnalyser:
    def __init__(self):
        try:
            os.mkdir(".temp")
        except OSError:
            pass

    def analyse(self, pomContents, use_direct_only = True, bbc_only = False):
        """
        Analyses the contents of [pom] and returns a list of ArtifactDependencyInfo objects.
        Uses maven to do the analysis.
        """
        pom_temporary_path_and_file_name = self._save_pom_contents_to_temporary_path(pomContents)
        tree_file = self._create_dependencies_text_file(pom_temporary_path_and_file_name, "tree.txt")
        artifact_dependency_info = self._make_artifactdependency_info_from(tree_file)
        return artifact_dependency_info

    def _maven_command(self):
        return "mvn dependency:tree -DoutputFile=tree.txt"

    def _save_pom_contents_to_temporary_path(self, pomContents):
        temp_file = open(".temp/pom.xml", "w")
        temp_file.writelines(pomContents)
        return ".temp/pom.xml"

    def _create_dependencies_text_file(self, pom_temporary_path_and_file_name, output_file_name):
        current_dir = os.getcwd()
        temporary_dir = os.path.dirname(pom_temporary_path_and_file_name)
        os.chdir(temporary_dir)
        print "Running maven on POM..."
        os.popen(self._maven_command())
        os.chdir(current_dir)
        tree_file = open(os.path.join(temporary_dir, output_file_name))
        return tree_file

    def _make_artifactdependency_info_from(self, tree_file):
        (artifact_info, depth) = self._parse_tree_line(tree_file.readline())
        dependencies = self._get_dependencies_from(tree_file)
        artifact_dependency_info = ArtifactDependencyInfo(artifact_info, dependencies)
        return artifact_dependency_info

    def _parse_tree_line(self, tree_line):
        """
        Takes a single tree_line from Maven and returns a 2-tuple of:"
        - the ArtifactInfo (name and version)
        - the depth of the artifact. 0 for the artifact being analysed, 1 for direct child, 2+ for indirect child
        """
        (indent_string, package_string) = self._split_tree_line_into_indent_and_package(tree_line)
        line_elements = package_string.split(":")
        depth = indent_string.count("+") + indent_string.count("|") + indent_string.count("\\")
        artifact_info_and_depth = (ArtifactInfo(":".join(line_elements[0:2]), line_elements[3]), depth)
        return artifact_info_and_depth

    def _get_dependencies_from(self, tree_file):
        dependencies = []
        for tree_line in tree_file.readlines():
            (artifact_info, depth) = self._parse_tree_line(tree_line)
            dependencies.append(ArtifactInfo(artifact_info.name, artifact_info.version, depth == 1))
        return dependencies

    def _split_tree_line_into_indent_and_package(self, tree_line):
        last_space = re.search('\w', tree_line).start() - 1
        indent_string = tree_line[:last_space].strip()
        package_string = tree_line[last_space + 1:].strip()
        return (indent_string, package_string)


##########################################################################################
# Tests

class PomAnalyserTest(unittest.TestCase):
    def setUp(self):
        self.pomAnalyser = PomAnalyser()

    def test_given_root_line_when_parse_tree_line_then_correct_name_and_version_and_level_are_returned(self):
        (artifact_info, level) = self.pomAnalyser._parse_tree_line("bbc.tvp.redbutton:redbutton-core:jar:2.0.0")
        self.assertEqual(artifact_info, ArtifactInfo("bbc.tvp.redbutton:redbutton-core", "2.0.0"))
        self.assertEqual(level, 0)

        (artifact_info, level) = self.pomAnalyser._parse_tree_line("columba:ristretto-common:jar:1.0:compile")
        self.assertEqual(artifact_info, ArtifactInfo("columba:ristretto-common", "1.0"))
        self.assertEqual(level, 0)

    def test_given_dependency_line_when_parse_tree_line_then_correct_name_and_version_and_level_are_returned(self):
        (artifact_info, level) = self.pomAnalyser._parse_tree_line("+- bbc.tvp.commons:tvp-commons-web:jar:2.1.0:compile")
        self.assertEqual(artifact_info, ArtifactInfo("bbc.tvp.commons:tvp-commons-web", "2.1.0"))
        self.assertEqual(level, 1)

        (artifact_info, level) = self.pomAnalyser._parse_tree_line("|  \- bbc.tvp.commons:tvp-commons-web:jar:2.1.0:compile")
        self.assertEqual(artifact_info, ArtifactInfo("bbc.tvp.commons:tvp-commons-web", "2.1.0"))
        self.assertEqual(level, 2)

        (artifact_info, level) = self.pomAnalyser._parse_tree_line("|  |  +- columba:ristretto-smtp:jar:1.0:compile")
        self.assertEqual(artifact_info, ArtifactInfo("columba:ristretto-smtp", "1.0"))
        self.assertEqual(level, 3)

    def test_given_dependency_line_with_comment_when_parse_tree_line_then_correct_name_and_version_and_level_are_returned(self):
        (artifact_info, level) = self.pomAnalyser._parse_tree_line("+- org.springframework:spring-test:jar:3.1.1.RELEASE:test (scope not updated to compile)")
        self.assertEqual(artifact_info, ArtifactInfo("org.springframework:spring-test", "3.1.1.RELEASE"))
        self.assertEqual(level, 1)


def do_integration_tests():
    pomFile = open("test/resources/simple_pom/pom.xml")
    pomContents = pomFile.readlines()
    analyser = PomAnalyser()

    artifact_dependency_info = analyser.analyse(pomContents)
    # print dependencyInfo
    print "Maven dependencies for", artifact_dependency_info.artifactInfo.name, "(version", artifact_dependency_info.artifactInfo.version, ")", "analysed"
    print "Dependencies are:"
    # pprint.pprint(artifact_dependency_info.dependencies)
    for dependency in artifact_dependency_info.dependencies:
        print dependency
    print "(end of dependencies)"


# If run as a program then run all the tests
if __name__ == "__main__":
    # unittest.main()
    do_integration_tests()
