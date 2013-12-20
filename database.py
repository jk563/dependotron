import schemaGenerator, MySQLdb
import pomanalyser
import artifactdependencyinfo


class Database:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database = 'dependotron'
        self.connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()
        self.cursor.close()

    def configure(self):
        """
        Tests if the database is there, builds it if not. Maybe throws exception if wrong schema?
        Alternatively this could be done in the constructor
        """
        generator = schemaGenerator.SchemaGenerator(self.host, self.user, self.password, self.database)
        generator.generateSchema()

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
        try:
            for descendant in artifactDependencyInfo.dependencies:
                self._addDescendant(artifactDependencyInfo.artifactInfo, descendant)
            self.connection.commit() # Commit transaction
        except:
            self.connection.rollback()
            raise

    def _addArtifactIfDoesNotExist(self, artifactInfo):
        try:
            addArtifactIdSQL = "INSERT INTO artifacts (artifact_name,artifact_version) VALUES ('%s','%s');" % \
                               (artifactInfo.name, artifactInfo.version)
            self.cursor.execute(addArtifactIdSQL)
            self.connection.commit()
        except:
            pass

    def _addDescendant(self, artifactInfo, descendantInfo):
        parentId = self._getArtifactId(artifactInfo)
        descendantId = self._getArtifactId(descendantInfo)
        addDependencySQL = "INSERT INTO dependencies (parent_id,descendant_id,direct_dependency) VALUES ('%s','%s','%d');" % \
                           (parentId, descendantId, descendantInfo.direct_dependency)
        try:
            self.cursor.execute(addDependencySQL)
        except:
            raise

    def _getArtifactId(self, artifactInfo):
        getArtifactIdSQL = "SELECT artifact_id FROM artifacts WHERE (artifact_name='%s' AND artifact_version='%s')" % \
                           (artifactInfo.name, artifactInfo.version)
        return self._getFromDatabase(getArtifactIdSQL)[0][0]

    def pomAnalysisExists(self, artifactInfo):
        numberOfDependenciesSQL = "SELECT COUNT(*) FROM dependencies WHERE parent_id = (SELECT artifact_id FROM artifacts WHERE artifact_name = '%s' and artifact_version = '%s')" % \
                                  (artifactInfo.name, artifactInfo.version)
        numberOfDependencies = self._getFromDatabase(numberOfDependenciesSQL)[0][0]
        return numberOfDependencies > 0

    def doesArtifactExist(self, artifactName, artifactVersion=None):
        return len(self.getArtifactInfo(artifactName, artifactVersion)) > 0

    def getArtifactInfo(self, artifactName, artifactVersion=None):
        if artifactVersion == None:
            existsSQL = "SELECT artifact_name,artifact_version FROM artifacts WHERE (artifact_name='%s')" % \
                        (artifactName)
        else:
            existsSQL = "SELECT artifact_name,artifact_version FROM artifacts WHERE (artifact_name='%s' AND artifact_version='%s')" % \
                        (artifactName, artifactVersion)
        return self._getFromDatabase(existsSQL,self.MySQLResultsToListOfArtifactInfo())

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
        self.cursor.execute(sql)
        sqlResult = self.cursor.fetchall()
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
    mySQLConnection = MySQLdb.connect(host='localhost', user='root', passwd='')
    mySqlCursor = mySQLConnection.cursor()
    deleteDependotronSQL = "DROP DATABASE dependotron;"
    try:
        mySqlCursor.execute(deleteDependotronSQL)
    except:
        pass

    gen = schemaGenerator.SchemaGenerator('localhost', 'root', '', 'dependotron')
    gen.generateSchema()
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