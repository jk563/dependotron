import MySQLdb


class SchemaGenerator:
    def generateSchema(self, host,user,password,database):
        mySQLConnection = MySQLdb.connect(host=host, user=user, passwd=password)
        self.createDependotronDatabaseIfExists(mySQLConnection, database)
        dependotronConnection = MySQLdb.connect(host=host, user=user, passwd=password, db=database)
        self.dependotronCursor = dependotronConnection.cursor()
        self.createTables()

    def createDependotronDatabaseIfExists(self, mySQLConnection,database):
        if(mySQLConnection):
            mySqlCursor = mySQLConnection.cursor()
            createDependotronSQL = "CREATE DATABASE IF NOT EXISTS " + database + ";"
            mySqlCursor.execute(createDependotronSQL)
        else:
            raise Exception("No MySQL connection set.")

    def createTables(self):
        if(self.dependotronCursor):
            artifactsSQL = "CREATE TABLE IF NOT EXISTS artifacts (artifact_id INT NOT NULL AUTO_INCREMENT, artifact_name VARCHAR(255) NOT NULL, artifact_version VARCHAR(31) NOT NULL, PRIMARY KEY (artifact_id), UNIQUE KEY (artifact_name,artifact_version));"
            dependenciesSQL = "CREATE TABLE IF NOT EXISTS dependencies (parent_id INT NOT NULL, descendant_id INT NOT NULL, direct_dependency BOOLEAN NOT NULL, FOREIGN KEY (parent_id) REFERENCES artifacts (artifact_id),FOREIGN KEY (descendant_id) REFERENCES artifacts (artifact_id));"
            self.dependotronCursor.execute(artifactsSQL)
            self.dependotronCursor.execute(dependenciesSQL)
        else:
            raise Exception("No dependotron connection set.")

if __name__ == '__main__':
    gen = SchemaGenerator()

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