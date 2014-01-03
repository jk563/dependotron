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
        if self._does_database_exist(self.database_name):
            connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd)
            cursor = connection.cursor()
            remove_database_query = 'DROP DATABASE %s' % self.database_name
            cursor.execute(remove_database_query)

    def test_connection_can_be_made(self):
        self.database_initialiser.connect_to_database()
        self.assertTrue(self.database_initialiser.connection)

    def test_database_created_if_it_does_not_exist(self):
        self.database_initialiser.connect_to_database()
        self.database_initialiser.initialise_database(self.database_name)
        self.assertTrue(self._does_database_exist(self.database_name), 'Database does not exist.')

    def _does_database_exist(self, database_name):
        connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd)
        cursor = connection.cursor()
        database_exists_query = "SELECT COUNT(SCHEMA_NAME) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME='%s'" \
                                % (database_name)
        cursor.execute(database_exists_query)
        number_of_results = cursor.fetchone()
        if number_of_results[0]== 1:
            return True
        else:
            return False