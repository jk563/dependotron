import schemaGenerator, MySQLdb
import pomanalyser

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
        self._addArtifact(artifactDependencyInfo.artifactInfo)
        for descendant in artifactDependencyInfo.dependencies:
            self._addDescendant(artifactDependencyInfo.artifactInfo,descendant)

    def _addArtifact(self, artifactTuple):
        artifactName = artifactTuple[0]
        artifactVersion = artifactTuple[1]
        dependotronConnection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.database)
        dependotronCursor = dependotronConnection.cursor()
        addArtifactIdSQL = "INSERT INTO artifacts (artifact_name,artifact_version) VALUES ('" + artifactName + "','" + artifactVersion + "');"
        try:
            dependotronCursor.execute(addArtifactIdSQL)
            dependotronConnection.commit()
        except:
            pass

    def _addDescendant(self, artifactTuple, descendantTuple):
        try:
            self._addArtifact(descendantTuple)
        except:
            pass
        parentId = str(self._getArtifactId(artifactTuple))
        descendantId = str(self._getArtifactId(descendantTuple))
        directDescendant = str(descendantTuple[2] | 0)
        dependotronConnection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.database)
        dependotronCursor = dependotronConnection.cursor()
        addDependencySQL = "INSERT INTO dependencies (parent_id,descendant_id,direct_dependency) VALUES ('" + parentId + "','" + descendantId + "','" + directDescendant + "');"
        try:
            dependotronCursor.execute(addDependencySQL)
            dependotronConnection.commit()
        except:
            pass

    def _getArtifactId(self,artifactTuple):
        artifactName = artifactTuple[0]
        artifactVersion = artifactTuple[1]
        dependotronConnection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.database)
        dependotronCursor = dependotronConnection.cursor()
        getArtifactIdSQL = "SELECT artifact_id FROM artifacts WHERE (artifact_name='" + artifactName + "' AND artifact_version='" + artifactVersion + "')"
        dependotronCursor.execute(getArtifactIdSQL)
        artifactId =  dependotronCursor.fetchall()[0][0]
        return artifactId

    def pomAnalysisExists(self,artifactTuple):
        artifactName = artifactTuple[0]
        artifactVersion = artifactTuple[1]
        dependotronConnection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.database)
        dependotronCursor = dependotronConnection.cursor()
        getArtifactIdSQL = "SELECT artifact_id FROM artifacts WHERE (artifact_name='" + artifactName + "' AND artifact_version='" + artifactVersion + "')"
        dependotronCursor.execute(getArtifactIdSQL)
        if(dependotronCursor.rowcount == 1):
            artifactId =  str(dependotronCursor.fetchall()[0][0])
            getParentSQL = "SELECT parent_id FROM dependencies WHERE (parent_id='" + artifactId + "')"
            dependotronCursor.execute(getArtifactIdSQL)
            if(dependotronCursor.rowcount ==1):
                return True
        return False


if __name__ == '__main__':
    gen = schemaGenerator.SchemaGenerator()

    mySQLConnection = MySQLdb.connect(host='localhost', user='root', passwd='')
    mySqlCursor = mySQLConnection.cursor()
    deleteDependotronSQL = "DROP DATABASE dependotron;"
    try:
        mySqlCursor.execute(deleteDependotronSQL)
    except:
        pass

    gen.generateSchema('localhost','root','','dependotron')
    dependotronConnection = MySQLdb.connect(host='localhost', user='root', passwd='', db='dependotron')
    dependotronCursor = dependotronConnection.cursor()

    db = Database()
    artifactDependencyInfo = pomanalyser.ArtifactDependencyInfo(('root','rootversion'),[('dep1','ver1', 1), ('dep2','ver1', 1), ('dep1','ver2', 0), ('dep1','ver2', 1), ('dep3','ver2', 1)])
    db.add(artifactDependencyInfo)