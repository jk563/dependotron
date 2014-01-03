import unittest
import schemaGenerator
import databaseinitialiser
import MySQLdb


class SchemaGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.host = 'localhost'
        self.user = 'root'
        self.passwd = ''
        self.database_name = 'schema_generator_test'
        database_initialiser = databaseinitialiser.DatabaseInitialiser(self.host, self.user, self.passwd)
        database_initialiser.initialise_database(self.database_name)

    def tearDown(self):
        database_exists_query = "SELECT COUNT(SCHEMA_NAME) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME='%s'" \
                                % (self.database_name)
        if self._get_number_of_results(database_exists_query) == 1:
            connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd)
            cursor = connection.cursor()
            remove_database_query = 'DROP DATABASE %s' % self.database_name
            cursor.execute(remove_database_query)
            cursor.close()
            connection.close()

    def test_database_contains_at_least_one_table(self):
        schema_generator = schemaGenerator.SchemaGenerator(self.host, self.user, self.passwd, self.database_name)
        schema_generator.generateSchema()
        number_of_tables_query = "SELECT COUNT(TABLE_NAME) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='%s'" \
                                % (self.database_name)
        number_of_tables = self._get_number_of_results(number_of_tables_query)
        self.assertGreater(number_of_tables, 0, 'No tables created.')

    def _get_number_of_results(self, query):
        connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd)
        cursor = connection.cursor()
        cursor.execute(query)
        number_of_results = cursor.fetchone()
        cursor.close()
        connection.close()
        return number_of_results[0]
