import schemaGenerator, MySQLdb

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


    def add(self, dependencyEntry):
        """
        Add new information to the database. [dependencyEntry] might be a tuple of:
        (dependencyName, dependencyVersion, dependentName, dependentVersion)
        """
        # dependotronConnection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.database)
        # dependotronCursor = dependotronConnection.cursor()
        # addDependencySQL = ''

    def addArtifact(self, artifactTuple):
        artifactName = artifactTuple[0]
        artifactVersion = artifactTuple[1]
        dependotronConnection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.database)
        dependotronCursor = dependotronConnection.cursor()
        addDependencySQL = "INSERT INTO artifacts (artifact_name,artifact_version) VALUES ('" + artifactName + "','" + artifactVersion + "');"
        dependotronCursor.execute(dependotronCursor)