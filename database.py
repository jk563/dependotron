import schemaGenerator, MySQLdb
import pomanalyser
import artifactdependencyinfo


class Database:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database = 'dependotron'

    def configure(self):
        """
        Tests if the database is there, builds it if not. Maybe throws exception if wrong schema?
        Alternatively this could be done in the constructor
        """
        generator = schemaGenerator.SchemaGenerator()
        generator.generateSchema(self.host, self.user, self.password, self.database)


    def add(self, artifactDependencyInfo):
        """
        Add new information to the database. [dependencyEntry] might be a tuple of:
        (dependencyName, dependencyVersion, dependentName, dependentVersion)
        """
        self._addArtifactIfDoesNotExist(artifactDependencyInfo.artifactInfo)
        for descendant in artifactDependencyInfo.dependencies:
            self._addArtifactIfDoesNotExist(descendant)
        try:
            self._addDependenciesTransaction(artifactDependencyInfo)
        except MySQLdb.Error:
            return False
        return True

    def _addDependenciesTransaction(self, artifactDependencyInfo):
        dependotronConnection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.database)
        dependotronCursor = dependotronConnection.cursor()
        for descendant in artifactDependencyInfo.dependencies:
            self._addDescendant(artifactDependencyInfo.artifactInfo, descendant, dependotronCursor)
        dependotronConnection.commit()
        dependotronCursor.close()
        dependotronConnection.close()

    def _addArtifactIfDoesNotExist(self, artifactInfo):
        try:
            addArtifactConnection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password,
                                                    db=self.database)
            addArtifactCursor = addArtifactConnection.cursor()
            addArtifactIdSQL = "INSERT INTO artifacts (artifact_name,artifact_version) VALUES ('%s','%s');" % \
                               (artifactInfo.name, artifactInfo.version)
            addArtifactCursor.execute(addArtifactIdSQL)
            addArtifactConnection.commit()
        except:
            pass

    def _addDescendant(self, artifactInfo, descendantInfo, cur):
        parentId = self._getArtifactId(artifactInfo)
        descendantId = self._getArtifactId(descendantInfo)
        addDependencySQL = "INSERT INTO dependencies (parent_id,descendant_id,direct_dependency) VALUES ('%s','%s','%s');" % \
                           (parentId, descendantId, descendantInfo.direct_dependency)
        try:
            cur.execute(addDependencySQL)
        except:
            raise

    def _getArtifactId(self, artifactInfo):
        artifactIdConnection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.database)
        artifactIdCursor = artifactIdConnection.cursor()
        getArtifactIdSQL = "SELECT artifact_id FROM artifacts WHERE (artifact_name='%s' AND artifact_version='%s')" % \
                           (artifactInfo.name, artifactInfo.version)
        artifactIdCursor.execute(getArtifactIdSQL)
        artifactId = artifactIdCursor.fetchall()[0][0]
        artifactIdCursor.close()
        artifactIdConnection.close()
        return artifactId

    def pomAnalysisExists(self, artifactInfo):
        pomExists = False
        pomAnalysisConnection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.database)
        pomAnalysisCursor = pomAnalysisConnection.cursor()
        getArtifactIdSQL = "SELECT artifact_id FROM artifacts WHERE (artifact_name='%s' AND artifact_version='%s')" % \
                           (artifactInfo.name, artifactInfo.version)
        pomAnalysisCursor.execute(getArtifactIdSQL)
        if (pomAnalysisCursor.rowcount == 1):
            artifactId = pomAnalysisCursor.fetchall()[0][0]
            getParentSQL = "SELECT DISTINCT parent_id FROM dependencies WHERE (parent_id='%s')" % \
                           (artifactId,)
            pomAnalysisCursor.execute(getParentSQL)
            if pomAnalysisCursor.rowcount == 1:
                pomExists = True
        pomAnalysisCursor.close()
        pomAnalysisConnection.close()
        return pomExists

    def doesArtifactExist(self, artifactName, artifactVersion=None):
        if len(self.getArtifactInfo(artifactName, artifactVersion)) != 0:
            return True
        else:
            return False

    def getArtifactInfo(self, artifactName, artifactVersion=None):
        artifactInfoConnection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.database)
        artifactInfoCursor = artifactInfoConnection.cursor()
        if artifactVersion == None:
            existsSQL = "SELECT artifact_name,artifact_version FROM artifacts WHERE (artifact_name='%s')" % \
                        (artifactName)
        else:
            existsSQL = "SELECT artifact_name,artifact_version FROM artifacts WHERE (artifact_name='%s' AND artifact_version='%s')" % \
                        (artifactName, artifactVersion)
        artifactInfoCursor.execute(existsSQL)
        artifacts = []
        for artifact in artifactInfoCursor.fetchall():
            artifacts.append(artifactdependencyinfo.ArtifactInfo(artifact[0],artifact[1]))
        artifactInfoCursor.close()
        artifactInfoConnection.close()
        return artifacts

    def getDownstreamDependencies(self, artifactInfo):
        if self.doesArtifactExist(artifactInfo.name, artifactInfo.version) == False:
            return None
        downstreamDependenciesConnection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.database)
        downstreamDependenciesCursor = downstreamDependenciesConnection.cursor()
        artifactId = self._getArtifactId(artifactInfo)
        existsSQL = "SELECT artifact_name,artifact_version FROM artifacts, dependencies WHERE (parent_id=%s AND artifact_id=descendant_id);" % \
                    (artifactId)
        downstreamDependenciesCursor.execute(existsSQL)
        artifacts = []
        for artifact in downstreamDependenciesCursor.fetchall():
            artifacts.append(artifactdependencyinfo.ArtifactInfo(artifact[0],artifact[1]))
        downstreamDependenciesCursor.close()
        downstreamDependenciesConnection.close()
        return artifactdependencyinfo.ArtifactDependencyInfo(artifactInfo, artifacts)
    
    def getUpstreamDependencies(self, artifactInfo):
        if self.doesArtifactExist(artifactInfo.name, artifactInfo.version) == False:
            return None
        upstreamDependenciesConnection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.database)
        upstreamDependenciesCursor = upstreamDependenciesConnection.cursor()
        artifactId = self._getArtifactId(artifactInfo)
        existsSQL = "SELECT artifact_name,artifact_version FROM artifacts, dependencies WHERE (descendant_id=%s AND artifact_id=parent_id);" % \
                    (artifactId)
        upstreamDependenciesCursor.execute(existsSQL)
        artifacts = []
        for artifact in upstreamDependenciesCursor.fetchall():
            artifacts.append(artifactdependencyinfo.ArtifactInfo(artifact[0],artifact[1]))
        upstreamDependenciesCursor.close()
        upstreamDependenciesConnection.close()
        return artifactdependencyinfo.ArtifactDependencyInfo(artifactInfo, artifacts)



if __name__ == '__main__':
    gen = schemaGenerator.SchemaGenerator()

    mySQLConnection = MySQLdb.connect(host='localhost', user='root', passwd='')
    mySqlCursor = mySQLConnection.cursor()
    deleteDependotronSQL = "DROP DATABASE dependotron;"
    try:
        mySqlCursor.execute(deleteDependotronSQL)
    except:
        pass

    gen.generateSchema('localhost', 'root', '', 'dependotron')
    dependotronConnection = MySQLdb.connect(host='localhost', user='root', passwd='', db='dependotron')
    dependotronCursor = dependotronConnection.cursor()

    db = Database()
    artifactDependencyInfo = pomanalyser.ArtifactDependencyInfo(
        artifactdependencyinfo.ArtifactInfo('root', 'rootversion'),
        [artifactdependencyinfo.ArtifactInfo('dep1', 'ver1', 1),
         artifactdependencyinfo.ArtifactInfo('dep2', 'ver1', 1),
         artifactdependencyinfo.ArtifactInfo('dep1', 'ver2', 1),
         artifactdependencyinfo.ArtifactInfo('dep3', 'ver2', 1)])

    db.add(artifactDependencyInfo)