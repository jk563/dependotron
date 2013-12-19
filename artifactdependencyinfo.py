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

class ArtifactInfo:
    def __init__(self, artifactName, artifactVersion, directDependency=0):
        self.artifactName = artifactName
        self.artifactVersion = artifactVersion
        self.directDependency = directDependency
