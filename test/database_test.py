import unittest
import database
import MySQLdb


class DatabaseTest(unittest.TestCase):

    def setUp(self):
        self.database = database.Database()
        self.database.cursor.close()
        self.database.connection.close()
        self.database.database = 'dependotron-test'
        self._databaseManipulation('CREATE')
        self.database.connection = MySQLdb.connect(host='%s', user='%s', passwd='', database='%s') \
                                                    % ('localhost','root', self.database.database)
        self.database.cursor = self.database.connection.cursor()

    def tearDown(self):
        self._databaseManipulation('DROP')

    def _databaseManipulation(self, command):
        mySQLConnection = MySQLdb.connect(host='localhost', user='root', passwd='')
        mySqlCursor = mySQLConnection.cursor()
        deleteDatabaseQuery = "%s DATABASE %s;" % (command, self.database.database)
        mySqlCursor.execute(deleteDatabaseQuery)
        mySqlCursor.close()
        mySQLConnection.close()

    def test_add_adds_dependencies_to_database(self):
        assert(True)

if __name__ == '__main__':
    unittest.main()