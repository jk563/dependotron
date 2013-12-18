import schemaGenerator

class Database:
    def __init__(self):
        pass

    def configure(self):
        """
        Tests if the database is there, builds it if not. Maybe throws exception if wrong schema?
        Alternatively this could be done in the constructor
        """
        generator = schemaGenerator.SchemaGenerator()
        generator.generateSchema('localhost','root','','dependotron')


    def add(self, dependencyEntry):
        """
        Add new information to the database. [dependencyEntry] might be a tuple of:
        (dependencyName, dependencyVersion, dependentName, dependentVersion)
        """
        pass