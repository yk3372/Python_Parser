from database.MySQLManager import MySQLManager

__author__ = 'yukai'

class BlogCategoryManager(MySQLManager):
    def create_blog_category(self):
        if self.connection is not None:
            cursor = self.connection.cursor()
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS `blog_category` (
                  `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
                  `name` VARCHAR(40) NOT NULL DEFAULT '',
                  PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                '''
            )
            self.connection.commit()
            cursor.close()

    def insert_into_blog_category(self, *values):
        if self.connection is not None:
            cursor = self.connection.cursor()
            for value in values:
                cursor.execute('insert into blog_category(name) VALUES (%s)', [value])
            self.connection.commit()
            cursor.close()

    def fetch_from_blog_category(self, query_id=None):
        if self.connection is not None:
            fetch_cursor = self.connection.cursor()
            if query_id is None:
                fetch_cursor.execute("select id,name from blog_category")
            else:
                fetch_cursor.execute("select id,name from blog_category WHERE id = %s", [query_id])
            values = fetch_cursor.fetchall()
            fetch_cursor.close()
            return values

if __name__ == '__main__':
    sqlManager = BlogCategoryManager()
    sqlManager.create_connection()
    sqlManager.create_blog_category()
    names = ['Python教程', 'JavaScript教程', 'Git教程']
    sqlManager.insert_into_blog_category(*names)
    print(sqlManager.fetch_from_blog_category())
    sqlManager.close_conn()
