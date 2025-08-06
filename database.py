import sqlite3
from tkinter import messagebox

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                year INTEGER,
                genre TEXT,
                cover_path TEXT,
                description TEXT,
                status TEXT DEFAULT 'Не прочитано',
                progress REAL DEFAULT 0.0,
                notes TEXT,
                review TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                director TEXT,
                year INTEGER,
                genre TEXT,
                cover_path TEXT,
                description TEXT,
                status TEXT DEFAULT 'Не просмотрено',
                progress REAL DEFAULT 0.0,
                notes TEXT,
                review TEXT
            )
        ''')
        self.conn.commit()

    def insert_book(self, data):
        query = '''INSERT INTO books 
            (title, author, year, genre, cover_path, description, status, progress, notes, review) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        try:
            self.cursor.execute(query, data)
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить книгу: {e}")

    # Аналогичные методы для фильмов, обновления, удаления...

    def fetch_all_books(self):
        self.cursor.execute("SELECT * FROM books")
        return self.cursor.fetchall()
    
    def fetch_all_movies(self):  # Новый метод
        self.cursor.execute("SELECT * FROM movies")
        return self.cursor.fetchall()
    
    def insert_element(self, element_type, title, author, year, genre, status):
        if element_type == 'book':
            query = '''INSERT INTO books 
                (title, author, year, genre, status) 
                VALUES (?, ?, ?, ?, ?)'''
        elif element_type == 'movie':
            query = '''INSERT INTO movies 
                (title, director, year, genre, status) 
                VALUES (?, ?, ?, ?, ?)'''
        self.cursor.execute(query, (title, author, year, genre, status))
        self.conn.commit()

    def update_element(self, element_type, element_id, title, author, year, genre, status):
        if element_type == 'book':
            query = '''UPDATE books SET 
                title=?, author=?, year=?, genre=?, status=? 
                WHERE id=?'''
        elif element_type == 'movie':
            query = '''UPDATE movies SET 
                title=?, director=?, year=?, genre=?, status=? 
                WHERE id=?'''
        self.cursor.execute(query, (title, author, year, genre, status, element_id))
        self.conn.commit()

    def delete_element(self, element_type, element_id):
        query = f"DELETE FROM {element_type}s WHERE id=?"
        self.cursor.execute(query, (element_id,))
        self.conn.commit()

    def insert_element(self, element_type, title, author, year, genre, status, progress):
        if element_type == 'book':
            query = '''INSERT INTO books 
                (title, author, year, genre, status, progress) 
                VALUES (?, ?, ?, ?, ?, ?)'''
        elif element_type == 'movie':
            query = '''INSERT INTO movies 
                (title, director, year, genre, status, progress) 
                VALUES (?, ?, ?, ?, ?, ?)'''
        self.cursor.execute(query, (title, author, year, genre, status, progress))
        self.conn.commit()

    def update_element(self, element_type, element_id, title, author, year, genre, status, progress):
        if element_type == 'book':
            query = '''UPDATE books SET 
                title=?, author=?, year=?, genre=?, status=?, progress=? 
                WHERE id=?'''
        elif element_type == 'movie':
            query = '''UPDATE movies SET 
                title=?, director=?, year=?, genre=?, status=?, progress=? 
                WHERE id=?'''
        self.cursor.execute(query, (title, author, year, genre, status, progress, element_id))
        self.conn.commit()

    def insert_book(self, title, author, year, genre, cover_path, 
                    description, status, progress, notes, review):
        query = '''INSERT INTO books 
            (title, author, year, genre, cover_path, description, 
            status, progress, notes, review) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        try:
            self.cursor.execute(query, (title, author, year, genre, cover_path,
                                    description, status, progress, notes, review))
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Ошибка добавления книги: {e}")
        
    def update_book(self, book_id, title, author, year, genre, cover_path,
                    description, status, progress, notes, review):
        query = '''UPDATE books SET 
            title=?, author=?, year=?, genre=?, cover_path=?, description=?, 
            status=?, progress=?, notes=?, review=? 
            WHERE id=?'''
        try:
            self.cursor.execute(query, (title, author, year, genre, cover_path,
                                    description, status, progress, notes, review, book_id))
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Ошибка обновления книги: {e}")
        
    def get_book_by_id(self, book_id):
        self.cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
        return self.cursor.fetchone()
    
    def insert_movie(self, title, director, year, genre, cover_path, 
                    description, status, progress, notes):
        query = '''INSERT INTO movies 
            (title, director, year, genre, cover_path, description, 
            status, progress, notes) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        try:
            self.cursor.execute(query, (title, director, year, genre, cover_path,
                                    description, status, progress, notes))
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Ошибка добавления фильма: {e}")
        
    def get_movie_by_id(self, movie_id):
        self.cursor.execute("SELECT * FROM movies WHERE id=?", (movie_id,))
        return self.cursor.fetchone()
    
    def update_movie(self, movie_id, title, director, year, genre, cover_path, 
                    description, status, progress, notes):
        query = '''UPDATE movies SET 
            title=?, director=?, year=?, genre=?, cover_path=?, description=?,
            status=?, progress=?, notes=?
            WHERE id=?'''
        try:
            self.cursor.execute(query, (title, director, year, genre, cover_path,
                                    description, status, progress, notes, movie_id))
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Ошибка обновления фильма: {e}")
        
        