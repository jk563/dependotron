import MySQLdb

class DatabaseInitialiser:
    def __init__(self, host, user, passwd):
        self.host = host
        self.user = user
        self.passwd = passwd

    def connect_to_database(self):
        self.connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd)
