__author__ = 'yukai'
import mysql.connector


class MySQLManager(object):
    user_name = "root"
    user_password = "1234"
    user_database = "yk_blog"
    connection = None

    def create_connection(self):
        self.connection = mysql.connector.connect(
            user=self.user_name,
            password=self.user_password,
            database=self.user_database
        )

    def close_conn(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
