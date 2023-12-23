import sqlite3

class DatabaseConnector:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER,
                text TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                link TEXT UNIQUE
            )
        ''')
        self.conn.commit()

    def add_message(self, message):
        self.cursor.execute('INSERT INTO messages (message_id, text) VALUES (?, ?)', (message.message_id, message.text))
        self.conn.commit()

    def get_all_messages(self):
        self.cursor.execute('SELECT * FROM messages')
        return self.cursor.fetchall()

    def add_link(self, link):
        # Проверяем, есть ли уже такая ссылка в базе данных
        self.cursor.execute('SELECT link FROM links WHERE link = ?', (link,))
        existing_link = self.cursor.fetchone()

        if not existing_link:
            self.cursor.execute('INSERT INTO links (link) VALUES (?)', (link,))
            self.conn.commit()
            print(f"Added link: {link}")
        else:
            print(f"Link '{link}' already exists")

    def get_all_links(self):
        self.cursor.execute('SELECT link FROM links ORDER BY link')
        return [row[0] for row in self.cursor.fetchall()]

    def close_connection(self):
        self.conn.close()
