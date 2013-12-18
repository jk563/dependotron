import MySQLdb


class SchemaGenerator:
    def generateSchema(self, host,user,password,database):
        mySQLConnection = MySQLdb.connect(host=host, user=user, passwd=password)
        self.createDependotronDatabaseIfExists(mySQLConnection)
        dependotronConnection = MySQLdb.connect(host=host, user=user, passwd=password, db=database)
        self.dependotronCursor = dependotronConnection.cursor()
        self.createTable()

    def setMySQLConnection(self,host,user,password):
        self.mySQLConnection = MySQLdb.connect(host=host, user=user, passwd=password)

    def createDependotronDatabaseIfExists(self, mySQLConnection):
        if(mySQLConnection):
            mySqlCursor = mySQLConnection.cursor()
            createDependotronSQL = "CREATE DATABASE IF NOT EXISTS dependotron;"
            mySqlCursor.execute(createDependotronSQL)
        else:
            raise Exception("No MySQL connection set.")

    def createTable(self):
        if(self.dependotronCursor):
            createDependotronSQL = "CREATE TABLE IF NOT EXISTS dependencies (dependantName VARCHAR(255), dependantVersion VARCHAR(15), dependencyName VARCHAR(255), dependencyVersion VARCHAR(15), directDependency BOOLEAN);"
            self.dependotronCursor.execute(createDependotronSQL)
        else:
            raise Exception("No dependotron connection set.")

if __name__ == '__main__':
    gen = SchemaGenerator()
    gen.generateSchema('localhost','root','','dependotron')