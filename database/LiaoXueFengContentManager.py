from database.MySQLManager import MySQLManager

__author__ = 'yukai'


class LiaoXueFengContentManager(MySQLManager):

    def create_content(self):
        if self.connection is not None:
            cursor = self.connection.cursor()
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS `liaoxuefeng_content` (
                  `parent_key` varchar(100) NOT NULL DEFAULT '',
                  `sub_key` varchar(100) NOT NULL DEFAULT '',
                  `content` text NOT NULL,
                  PRIMARY KEY (`parent_key`,`sub_key`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                '''
            )
            self.connection.commit()
            cursor.close()

    def insert_into_content(self, *values):
        if self.connection is not None:
            cursor = self.connection.cursor()
            cursor.execute(
                '''
                insert into `liaoxuefeng_content` (`parent_key`, `sub_key`, `content`)
                VALUES (%s, %s, %s)
                ''',
                values)
            self.connection.commit()
            cursor.close()

    def fetch_from_content(self):
        if self.connection is not None:
            fetch_cursor = self.connection.cursor()
            fetch_cursor.execute("SELECT * FROM `liaoxuefeng_content` LIMIT 1")
            values = fetch_cursor.fetchall()
            fetch_cursor.close()
            return values


if __name__ == '__main__':
    sqlManager = LiaoXueFengContentManager()
    sqlManager.create_connection()
    sqlManager.create_content()
    sqlManager.insert_into_content(*['parent_key', 'sub_key', 'content'])
    print(sqlManager.fetch_from_content())
    sqlManager.close_conn()
