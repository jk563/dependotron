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
            cursor.close()
            connection.close()

    def test_database_created(self):
        self.database_initialiser.initialise_database(self.database_name)
        database_exists_query = "SELECT COUNT(SCHEMA_NAME) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME='%s'" \
                                % (self.database_name)
        self.assertTrue(self._get_number_of_results(database_exists_query) == 1, 'Database does not exist.')

    # Duplicate Code
    def _get_number_of_results(self, query):
        connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd)
        cursor = connection.cursor()
        cursor.execute(query)
        number_of_results = cursor.fetchone()
        cursor.close()
        connection.close()
        return number_of_results[0]
