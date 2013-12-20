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

    # TODO : Use private get from database and formatter
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
        addDependencySQL = "INSERT INTO dependencies (parent_id,descendant_id,direct_dependency) VALUES ('%s','%s','%d');" % \
                           (parentId, descendantId, descendantInfo.direct_dependency)
        try:
            cur.execute(addDependencySQL)
        except:
            raise

    # TODO : Use private get from database and formatter
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

    # TODO : Use private get from database and formatter
    def pomAnalysisExists(self, artifactInfo):
        # This sql will do the query in one go
        # sql = "SELECT COUNT(*) FROM dependencies WHERE parent_id = (SELECT artifact_id FROM artifacts WHERE artifact_name = '%s' and artifact_version = '%s')"
        # sql = sql % (artifactInfo.name, artifactInfo.version)
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

    # TODO : Use private get from database and formatter
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
        artifactId = self._getArtifactId(artifactInfo)
        downstreamSql = "SELECT artifact_name,artifact_version, direct_dependency FROM artifacts, dependencies WHERE (parent_id=%s AND artifact_id=descendant_id);" % \
                    (artifactId)
        dependencies = self._getFromDatabase(downstreamSql,self.MySQLResultsToListOfArtifactInfo())
        return artifactdependencyinfo.ArtifactDependencyInfo(artifactInfo, dependencies)
    
    def getUpstreamDependencies(self, artifactInfo):
        if self.doesArtifactExist(artifactInfo.name, artifactInfo.version) == False:
            return None
        artifactId = self._getArtifactId(artifactInfo)
        upstreamSql = "SELECT artifact_name,artifact_version, direct_dependency FROM artifacts, dependencies WHERE (descendant_id=%s AND artifact_id=parent_id);" % \
                    (artifactId)
        dependencies = self._getFromDatabase(upstreamSql, self.MySQLResultsToListOfArtifactInfo())
        return artifactdependencyinfo.ArtifactDependencyInfo(artifactInfo, dependencies)

    def _getFromDatabase(self, sql, formatter=None):
        databaseConnection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.database)
        databaseCursor = databaseConnection.cursor()
        databaseCursor.execute(sql)
        sqlResult = databaseCursor.fetchall()
        databaseCursor.close()
        databaseConnection.close()
        if formatter:
            if formatter.format:
                return formatter.format(sqlResult)
            else:
                raise FormatterException
        return sqlResult

    class MySQLResultsToListOfArtifactInfo:
        def format(self, mysqlResults):
            formatter = TupleToArtifactInfoFormatter()
            result = []
            for mysqlTuple in mysqlResults:
                result.append(formatter.format(mysqlTuple))
            return result


class TupleToArtifactInfoFormatter:
    def format(self, tupleToFormat):
        if len(tupleToFormat) is 3:
            return artifactdependencyinfo.ArtifactInfo(tupleToFormat[0],tupleToFormat[1], tupleToFormat[2])
        elif len(tupleToFormat) is 2:
            return artifactdependencyinfo.ArtifactInfo(tupleToFormat[0],tupleToFormat[1])
        else:
            raise FormatterException


class FormatterException(Exception):
    pass

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