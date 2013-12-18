import MySQLdb


class SchemaGenerator:
    def generateSchema(self, host,user,password,database):
        mySQLConnection = MySQLdb.connect(host=host, user=user, passwd=password)
        self.createDependotronDatabaseIfExists(mySQLConnection, database)
        dependotronConnection = MySQLdb.connect(host=host, user=user, passwd=password, db=database)
        self.dependotronCursor = dependotronConnection.cursor()
        self.createTables()

    def setMySQLConnection(self,host,user,password):
        self.mySQLConnection = MySQLdb.connect(host=host, user=user, passwd=password)

    def createDependotronDatabaseIfExists(self, mySQLConnection,database):
        if(mySQLConnection):
            mySqlCursor = mySQLConnection.cursor()
            createDependotronSQL = "CREATE DATABASE IF NOT EXISTS " + database + ";"
            mySqlCursor.execute(createDependotronSQL)
        else:
            raise Exception("No MySQL connection set.")

    def createTables(self):
        if(self.dependotronCursor):
            artifactsSQL = "CREATE TABLE IF NOT EXISTS artifacts (id INT NOT NULL AUTO_INCREMENT, artifact_name VARCHAR(255) NOT NULL, artifact_version VARCHAR(31) NOT NULL, PRIMARY KEY (id));"
            dependenciesSQL = "CREATE TABLE IF NOT EXISTS dependencies (parent_id INT NOT NULL, descendant_id INT NOT NULL, direct_dependency BOOLEAN NOT NULL, FOREIGN KEY (parent_id) REFERENCES artifacts (id),FOREIGN KEY (descendant_id) REFERENCES artifacts (id));"
            self.dependotronCursor.execute(artifactsSQL)
            self.dependotronCursor.execute(dependenciesSQL)
        else:
            raise Exception("No dependotron connection set.")

if __name__ == '__main__':
    gen = SchemaGenerator()

    mySQLConnection = MySQLdb.connect(host='localhost', user='root', passwd='')
    mySqlCursor = mySQLConnection.cursor()
    deleteDependotronSQL = "DROP DATABASE dependotron;"
    mySqlCursor.execute(deleteDependotronSQL)

    gen.generateSchema('localhost','root','','dependotron')