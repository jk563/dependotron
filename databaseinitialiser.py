import MySQLdb

class DatabaseInitialiser:
    def __init__(self, host, user, passwd):
        self.host = host
        self.user = user
        self.passwd = passwd

    def connect_to_database(self):
        self.connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd)

    def initialise_database(self, database):
        cursor = self.connection.cursor()
        create_database_sql = 'CREATE DATABASE IF NOT EXISTS %s;' % (database)
        cursor.execute(create_database_sql)
        self.connection.commit()