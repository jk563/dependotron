import unittest, xml.etree.ElementTree as ET
from pomProcessor import PomProcessor


class pomProcessorTest(unittest.TestCase):

    def setUp(self):
        testPom = ET.parse('resources/xml/basicPom.xml')
        self.pomProcessor = PomProcessor(testPom)

    def tearDown(self):
        self.pomProcessor = None

    def test_InitSetsPom(self):
        expectedElementTree = ET.Element('')
        pomProcessor = PomProcessor(expectedElementTree)
        actualElementTree = pomProcessor.pom
        assert(actualElementTree == expectedElementTree)

    def test_getPomArtifactIdReturnPomArtifactId(self):
        expectedArtifactId = 'pomArtifactId'
        actualArtifactId = self.pomProcessor.getPomArtifactId()
        assert(actualArtifactId == expectedArtifactId)

    def test_getPomGroupIdReturnPomGroupId(self):
        expectedGroupId = 'pomGroupId'
        actualGroupId = self.pomProcessor.getPomGroupId()
        assert(actualGroupId == expectedGroupId)

    def test_getParentArtifactIdReturnsParentGroupId(self):
        expectedArtifactId = 'parentGroupId'
        actualArtifactId = self.pomProcessor.getParentArtifactId()
        assert(actualArtifactId == expectedArtifactId)

    def test_getParentArtifactIdReturnsParentGroupId(self):
        expectedGroupId = 'parentGroupId'
        actualGroupId = self.pomProcessor.getParentGroupId()
        assert(actualGroupId == expectedGroupId)

if __name__ == '__main__':
    unittest.main()