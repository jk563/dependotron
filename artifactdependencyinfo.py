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
    def __init__(self, artifact_name, artifact_version, direct_dependency=0):
        self.name = artifact_name
        self.version = artifact_version
        self.direct_dependency = direct_dependency

    def __eq__(self, other):
        return self.name == other.name and \
            self.version == other.version and \
            self.direct_dependency == other.direct_dependency

    def __str__(self):
        return "<->".join([self.name, self.version, str(self.direct_dependency)])
