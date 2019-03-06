import sqlite3


class DB:
    def __init__(self):
        conn = sqlite3.connect('users.db', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class BaseUs:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         user_name VARCHAR(50),
                         password_hash VARCHAR(128)
                         )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users
                      (user_name, password_hash)
                      VALUES (?,?)''', (user_name, password_hash))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                    (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)


class BaseNe:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         user_name VARCHAR(50),
                         password_hash VARCHAR(128)
                         )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, text):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO news
                      (user_name, password_hash)
                      VALUES (?,?)''', (title, text))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news WHERE id = ?", (str(user_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news")
        rows = cursor.fetchall()
        return rows

    def exists(self, title, text):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news WHERE title = ? AND text = ?",
                    (title, text))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)
