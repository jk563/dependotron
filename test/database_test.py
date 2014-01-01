import unittest
import database
import MySQLdb


class DatabaseTest(unittest.TestCase):

    def setUp(self):
        self.database = database.Database()
        self.database.cursor.close()
        self.database.connection.close()
        self.database.database = 'dependotron-test'
        mySQLConnection = MySQLdb.connect(host='localhost', user='root', passwd='')
        mySqlCursor = mySQLConnection.cursor()
        createDatabaseQuery = "CREATE DATABASE %s;" % (self.database.database)
        mySqlCursor.execute(createDatabaseQuery)
        self.database.connection = MySQLdb.connect(host='%s', user='%s', passwd='', database='%s') \
                                                    % ('localhost','root', self.database.database)
        self.database.cursor = self.database.connection.cursor()

    def add_adds_dependencies_to_database(self):
        pass

if __name__ == '__main__':
    unittest.main()