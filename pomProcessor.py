try :
    import elementtree.ElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from artifactdependencyinfo import ArtifactInfo

class PomProcessor:
    def __init__(self, pom_analyser, database):
        self._pom_analyser = pom_analyser
        self._database = database

    def update(self, pom_content_string):
        pom_tree = ET.fromstring(pom_content_string)
        artifactInfo = self._create_info_from_pom_tree(pom_tree)
        if not self._database.pomAnalysisExists(artifactInfo):
            artifact_dependency_info = self._pom_analyser.analyse(pom_content_string, True)
            self._database.add(artifact_dependency_info)

    def _create_info_from_pom_tree(self, pom_tree):
        artifact_info = ArtifactInfo(self._get_artifact_name(pom_tree), self._get_artifact_version(pom_tree))
        return artifact_info

    def _get_artifact_name(self, pom_tree):
        return self._get_group_id(pom_tree) + "." + self._get_artifact_id(pom_tree)

    def _get_artifact_id(self, pom_tree):
        attribute = pom_tree.find('{http://maven.apache.org/POM/4.0.0}artifactId')
        return attribute.text

    def _get_group_id(self, pom_tree):
        attribute = pom_tree.find('{http://maven.apache.org/POM/4.0.0}groupId')
        return attribute.text

    def _get_artifact_version(self, pom_tree):
        attribute = pom_tree.find('{http://maven.apache.org/POM/4.0.0}version')
        return attribute.text
