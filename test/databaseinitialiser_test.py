import unittest
import MySQLdb
import databaseinitialiser

class DatabaseInitialiserTest(unittest.TestCase):
    def setUp(self):
        self.host = 'localhost'
        self.user = 'root'
        self.passwd = ''
        self.database_initialiser = databaseinitialiser.DatabaseInitialiser(self.host, self.user, self.passwd)
        self.database_name = 'database_initialiser_test'

    def tearDown(self):
        if self._does_database_exist():
            connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd)
            cursor = connection.cursor()
            remove_database_query = 'DROP DATABASE %s' % self.database_name
            cursor.execute(remove_database_query)

    def test_database_created(self):
        self.database_initialiser.connect_to_database()
        self.database_initialiser.initialise_database(self.database_name)
        self.assertTrue(self._does_database_exist(), 'Database does not exist.')

    def _does_database_exist(self):
        connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd)
        cursor = connection.cursor()
        database_exists_query = "SELECT COUNT(SCHEMA_NAME) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME='%s'" \
                                % (self.database_name)
        cursor.execute(database_exists_query)
        number_of_results = cursor.fetchone()
        if number_of_results[0]== 1:
            return True
        else:
            return False