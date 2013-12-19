import unittest
from pomProcessor import PomProcessor


class PomProcessorTest(unittest.TestCase):

    def setUp(self):
        self._pom_content = open('resources/xml/basicPom.xml', "r").read()
        self._pom_fetcher = None
        self._pom_analyser = None
        self._database = None

    def tearDown(self):
        self._pom_content = None
        self._pom_fetcher = None
        self._pom_analyser = None
        self._database = None
        self.pomProcessor = None

    def test_database_asked_if_correct_artifact_analysis_exists(self):
        self._database = TestDatabaseAnalysisExists()
        self._pom_processor = PomProcessor(self._pom_fetcher, self._pom_analyser, self._database)

        self._pom_processor.update(self._pom_content)
        self.assertEqual("pomGroupId.pomArtifactId", self._database.get_artifact_info().artifactName)
        self.assertEqual("0.1.0", self._database.get_artifact_info().artifactVersion)

    def test_output_of_analysis_written_to_database(self):
        dependency_info = "something"
        self._pom_analyser = TestPomAnalyser(dependency_info)
        self._database = TestDatabaseAnalysisNotExists()
        self._pom_processor = PomProcessor(self._pom_fetcher, self._pom_analyser, self._database)

        self._pom_processor.update(self._pom_content)
        self.assertEqual(dependency_info, self._database.get_artifact_dependency_info())

class TestDatabaseAnalysisExists:
    def __init__(self):
        self._artifactInfo = None

    def pomAnalysisExists(self, artifactInfo):
        self._artifactInfo = artifactInfo
        return True

    def get_artifact_info(self):
        return self._artifactInfo

class TestDatabaseAnalysisNotExists:
    def __init__(self):
        self._artifact_dependency_info = None

    def pomAnalysisExists(self, artifact_info):
        return False

    def add(self, artifact_dependency_info):
        self._artifact_dependency_info = artifact_dependency_info

    def get_artifact_dependency_info(self):
        return self._artifact_dependency_info

class TestPomAnalyser:

    def __init__(self, artifact_dependency_info):
        self._artifact_dependency_info = artifact_dependency_info

    def analyse(self, artifact_info, direct_only = False):
        return self._artifact_dependency_info


if __name__ == '__main__':
    unittest.main()