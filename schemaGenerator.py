import MySQLdb


class SchemaGenerator:
    def __init__(self,host,user,password,database):
        self.database = database
        self.dbConnection = MySQLdb.connect(host=host, user=user, passwd=password)
        self.dbCursor = self.dbConnection.cursor()
        self.createDependotronDatabaseIfNotExists()
        self.dbCursor.close()
        self.dbConnection.close()
        self.dependotronConnection = MySQLdb.connect(host=host, user=user, passwd=password, db=database)
        self.dependotronCursor = self.dependotronConnection.cursor()

    def __del__(self):
        self.dependotronCursor.close()
        self.dependotronConnection.close()

    def generateSchema(self):
        artifactsSQL = """CREATE TABLE IF NOT EXISTS artifacts
                        (artifact_id INT NOT NULL AUTO_INCREMENT, artifact_name VARCHAR(255) NOT NULL,
                        artifact_version VARCHAR(31) NOT NULL,
                        PRIMARY KEY (artifact_id), UNIQUE KEY (artifact_name,artifact_version));"""
        dependenciesSQL = """CREATE TABLE IF NOT EXISTS dependencies
                        (parent_id INT NOT NULL, descendant_id INT NOT NULL, direct_dependency BOOLEAN NOT NULL,
                        FOREIGN KEY (parent_id) REFERENCES artifacts (artifact_id),
                        FOREIGN KEY (descendant_id) REFERENCES artifacts (artifact_id),UNIQUE KEY
                        (parent_id,descendant_id));"""
        self.dependotronCursor.execute(artifactsSQL)
        self.dependotronCursor.execute(dependenciesSQL)

    def createDependotronDatabaseIfNotExists(self):
        createDependotronSQL = "CREATE DATABASE IF NOT EXISTS " + self.database + ";"
        self.dbCursor.execute(createDependotronSQL)
        self.dbConnection.commit()


if __name__ == '__main__':

    mySQLConnection = MySQLdb.connect(host='localhost', user='root', passwd='')
    mySqlCursor = mySQLConnection.cursor()
    deleteDependotronSQL = "DROP DATABASE dependotron;"
    try:
        mySqlCursor.execute(deleteDependotronSQL)
    except:
        pass
    mySqlCursor.close()
    mySQLConnection.close()

    gen = SchemaGenerator('localhost','root','','dependotron')
    gen.generateSchema()