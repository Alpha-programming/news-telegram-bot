import sqlite3
from pathlib import Path
import requests

BASE_DIR = Path(__name__).resolve().parent


class DatabaseConnection:
    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self.cursor, self.connection = self.connect()


    def connect(self) -> tuple[sqlite3.Cursor, sqlite3.Connection]:
        connection = sqlite3.connect(BASE_DIR / self.database_path)
        cursor = connection.cursor()
        return cursor, connection

class DatabaseTables(DatabaseConnection):
    def __init__(self, database_path: str) -> None:
        super().__init__(database_path)

    def create(self, query:str) -> None:
        self.cursor.executescript(query)

db_table = DatabaseTables('database.db')
db_table.create('''
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id BIGINT UNIQUE
);

CREATE TABLE IF NOT EXISTS news(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    author TEXT,
    title TEXT,
    description TEXT,
    url TEXT,
    published_at DATETIME,
    content TEXT,
    user_id INTEGER REFERENCES users(id)
);
''')

class UsersRepo(DatabaseConnection):
    def get_user(self, chat_id: int) -> tuple | None:
        self.cursor.execute("SELECT id FROM users WHERE chat_id = ?;", (chat_id,))
        result = self.cursor.fetchone()
        return result

    def add_user(self, chat_id:int) -> None:
        query = 'INSERT INTO users(chat_id) VALUES (?);'

        if self.get_user(chat_id) is None:
            self.cursor.execute(query, (chat_id,))
            self.connection.commit()

from datetime import datetime

class NewsRepo(DatabaseConnection):
    def reset_autoincrement(self):
        reset_query = 'DELETE FROM sqlite_sequence WHERE name="news";'
        self.cursor.execute(reset_query)
        self.connection.commit()

    def delete_news(self, user_id):
        delete_query = '''
                    DELETE FROM news
                    WHERE user_id = ?;
                '''
        self.cursor.execute(delete_query, (user_id,))
        self.connection.commit()
        self.reset_autoincrement()

    def add_news(self,
                 name: str,
                 author: str,
                 title: str,
                 description: str,
                 url: str,
                 published_at: datetime,
                 content: str,
                 user_id: int,
                 ):

        check_query = '''
            SELECT COUNT(*) FROM news
            WHERE user_id = ? AND content = ?
        '''
        self.cursor.execute(check_query,(user_id,content,))
        count = self.cursor.fetchone()[0]

        if count == 0:
            query = ('''INSERT INTO news(name,author,title,description,url,published_at,content,user_id)
            VALUES(?,?,?,?,?,?,?,?);
            ''')
            self.cursor.execute(query,(name,author,title,description,url,published_at,content,user_id))
            self.connection.commit()

    def get_news(self, user_id):
        query = 'SELECT name,author,title,description,url,published_at,content FROM news WHERE user_id = ?'
        result = self.cursor.execute(query,(user_id,)).fetchall()
        if result:
            return result
        return None

users_repo = UsersRepo(BASE_DIR/'database.db')
news_repo = NewsRepo(BASE_DIR/'database.db')