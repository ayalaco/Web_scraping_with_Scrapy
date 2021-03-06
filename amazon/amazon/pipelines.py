# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
import mysql.connector


class SQLlitePipeline:

    def open_spider(self, spider):
        """
        Opens a connection to the database and creates a new table if one does not exist yet.
        """
        self.connection = sqlite3.connect("amazon.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE product_reviews(
                    product_name TEXT,
                    product_url TEXT,
                    product_ingredients TEXT,
                    review_title TEXT,
                    review_body TEXT,
                    rating REAL
                )
            
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        """
        Terminates connection to the database when finished.
        """
        self.connection.close()

    def process_item(self, item: dict, spider) -> dict:
        """
        Inserts the scraped data from one item into the database.
        """
        self.c.execute('''
            INSERT INTO product_reviews (product_name,product_url,product_ingredients,review_title,review_body,rating) 
            VALUES(?,?,?,?,?,?)

        ''', (
            item.get('product_name'),
            item.get('product_url'),
            item.get('product_ingredients'),
            item.get('review_title'),
            item.get('review_body'),
            item.get('rating')
        ))
        self.connection.commit()
        return item


class mySQLPipeline:

    def open_spider(self, spider):
        """
        Opens a connection to the database and creates a new table if one does not exist yet.
        """
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='input_your_password here',
            database='name_of_our_db'  # create it in mySQL beforehand
        )
        self.c = self.connection.cursor()

        self.c.execute('''
            CREATE TABLE IF NOT EXISTS product_reviews(
                product_name TEXT,
                product_url TEXT,
                product_ingredients TEXT,
                review_title TEXT,
                review_body TEXT,
                rating REAL
            )
        
        ''')
        self.connection.commit()


    def close_spider(self, spider):
        """
        Terminates connection to the database when finished.
        """
        self.connection.close()

    def process_item(self, item: dict, spider) -> dict:
        """
        Inserts the scraped data from one item into the database.
        """
        self.c.execute('''
            INSERT INTO product_reviews (product_name,product_url,product_ingredients,review_title,review_body,rating) 
            VALUES(%s,%s,%s,%s,%s,%s)

        ''', (
            item.get('product_name'),
            item.get('product_url'),
            item.get('product_ingredients'),
            item.get('review_title'),
            item.get('review_body'),
            item.get('rating')
        ))
        self.connection.commit()
        return item
