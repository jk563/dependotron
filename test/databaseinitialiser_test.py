import unittest
import databaseinitialiser

class DatabaseInitialiserTest(unittest.TestCase):
    def setUp(self):
      host = 'localhost'
      user = 'root'
      passwd = ''
      self.database_initialiser = databaseinitialiser.DatabaseInitialiser(host, user, passwd)

    def test_connection_can_be_made(self):
      self.database_initialiser.connect_to_database()
      self.assertTrue(self.database_initialiser.connection)

    