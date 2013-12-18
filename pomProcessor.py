import xml.etree.ElementTree as ET

class PomProcessor:
    def __init__(self, pomTree):
        self.pom = pomTree

    def getPomArtifactId(self):
        return self.__getArtifactId(self.pom)

    def getPomGroupId(self):
        return self.__getGroupId(self.pom)

    def getParentArtifactId(self):
        parentElement = self.pom.find('{http://maven.apache.org/POM/4.0.0}parent')
        return self.__getArtifactId(parentElement)

    def getParentGroupId(self):
        parentElement = self.pom.find('{http://maven.apache.org/POM/4.0.0}parent')
        return self.__getGroupId(parentElement)

    def __getArtifactId(self, element):
        artifactIdAttribute = element.find('{http://maven.apache.org/POM/4.0.0}artifactId')
        return artifactIdAttribute.text

    def __getGroupId(self, element):
        groupIdAttribute = element.find('{http://maven.apache.org/POM/4.0.0}groupId')
        return groupIdAttribute.text