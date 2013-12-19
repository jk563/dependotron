"""
Takes the contents of a pom file and, using Maven, determines the dependencies.
Depends on:
    - Maven: to interface with its repository and determine dependencies
Does not depend on!
    - SVN: we get given the contents of the POM directly, regardless of where it came from
"""
import unittest
import tempfile
import os
import pprint


class ArtifactDependencyInfo:
    """
    Simple wrapper around the following directory.
    from ((name, version), [(name, version, direct), ...)])
        artifactInfo is a tuple: (name, version)
        dependencies is a list: [(name1, version1, directFlag), ..., (nameN, versionN, directFlagN)]
    """
    def __init__(self, artifactInfo, dependencies):
        self.artifactInfo = artifactInfo
        self.dependencies = dependencies


class PomAnalyser:
    def __init__(self):
        try:
            os.mkdir(".temp")
        except OSError:
            pass

    def analyse(self, pomContents, use_direct_only = True):
        """
        Analyses the contents of [pom] and returns a list of tuples of dependencies.
        Uses maven to do the analysis.
        Returns an ArtifactDependencyInfo
        """
        pom_temporary_path_and_file_name = self._save_pom_contents_to_temporary_path(pomContents)
        tree_file = self._create_dependencies_text_file(pom_temporary_path_and_file_name, "tree.txt")
        self._make_artifactdependency_info_from(tree_file)
        return ArtifactDependencyInfo("", [])

    def _maven_command(self):
        return "mvn dependency:tree -DoutputFile=tree.txt"

    def _save_pom_contents_to_temporary_path(self, pomContents):
        temp_file = open(".temp/pom.xml", "w")
        temp_file.writelines(pomContents)
        return ".temp/pom.xml"

    def _create_dependencies_text_file(self, pom_temporary_path_and_file_name, output_file_name):
        current_dir = os.getcwd()
        temporary_dir =os.path.dirname(pom_temporary_path_and_file_name)
        os.chdir(temporary_dir)
        print "Running maven on POM..."
        os.popen(self._maven_command())
        os.chdir(current_dir)
        print "*****", temporary_dir
        tree_file = open(os.path.join(temporary_dir, output_file_name))
        return tree_file

    def _make_artifactdependency_info_from(self, tree_file):
        artifact_info = self._parse_tree_line(tree_file.readline())
        print "Maven dependencies for", artifact_info[0], "(version", artifact_info[1], ") analysed"

    def _parse_tree_line(self, tree_line):
        return ("redbutton_super_library", "1.2.3")


# If run as a program then run unit tests
if __name__ == "__main__":
    pomFile = open("test/resources/simple_pom/pom.xml")
    pomContents = pomFile.readlines()
    analyser = PomAnalyser()

    dependencyInfo = analyser.analyse(pomContents)
    print dependencyInfo
