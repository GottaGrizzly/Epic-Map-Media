import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from database import Database
from gui.add_window import AddBookWindow, AddElementWindow, AddMovieWindow

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.db = Database('library.db')
        self.create_ui()

    def open_add_book(self):
        AddElementWindow(self.root, "book")

    def edit_element(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        item_values = self.tree.item(selected_item)['values']
        element_id = self.tree.item(selected_item)['text']
        
        # Определите тип элемента (книга или фильм)
        element_type = "book" if item_values[0] == "Книга" else "movie"
        
        if element_type == "book":
            book_data = self.db.get_book_by_id(element_id)
            if book_data:
                AddBookWindow(self.root, self.db, parent=self, book_data=book_data)
        else:
            movie_data = self.db.get_movie_by_id(element_id)
            if movie_data:
                AddMovieWindow(self.root, self.db, parent=self, movie_data=movie_data)

    def delete_element(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        item_values = self.tree.item(selected_item)['values']
        element_id = self.tree.item(selected_item)['text']
        element_type = "book" if item_values[0] == "Книга" else "movie"
        self.db.delete_element(element_type, element_id)
        self.load_data()

    def on_double_click(self, event):
        self.edit_element()

    def create_ui(self):
        # Меню
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        
        file_menu = tk.Menu(menu)
        menu.add_cascade(label="Добавить", menu=file_menu)
        file_menu.add_command(label="Добавить книгу", command=self.open_add_book)
        file_menu.add_command(label="Добавить фильм", command=self.open_add_movie)
        

        # Фильтры
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(pady=10)
        
        self.status_var = tk.StringVar()
        statuses = ["Все", "Прочитано", "Просмотрено", "В процессе"]
        ttk.Combobox(filter_frame, textvariable=self.status_var, values=statuses).pack(side=tk.LEFT)
        ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter).pack(side=tk.LEFT)

        # Список элементов
        self.tree = ttk.Treeview(self.root, columns=("type", "title", "author/director", "year", "status"))
        self.tree.heading("#0", text="")
        self.tree.heading("type", text="Тип")
        self.tree.heading("title", text="Название")
        self.tree.heading("author/director", text="Автор/Режиссер")
        self.tree.heading("year", text="Год")
        self.tree.heading("status", text="Статус")
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.pack(fill=tk.BOTH, expand=True)

        edit_btn = ttk.Button(filter_frame, text="Редактировать", command=self.edit_element)
        edit_btn.pack(side=tk.LEFT)
        delete_btn = ttk.Button(filter_frame, text="Удалить", command=self.delete_element)
        delete_btn.pack(side=tk.LEFT)

        # Загрузка данных
        self.load_data()

    def show_statistics(self):
        stats = self.db.get_statistics()
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Статистика")
        
        # Вывод результатов
        ttk.Label(stats_window, text=f"Прочитано: {stats['books_read']} / {stats['total_books']} ({stats['books_percent']:.1f}%)").pack()
        ttk.Label(stats_window, text=f"Просмотрено: {stats['movies_watched']} / {stats['total_movies']} ({stats['movies_percent']:.1f}%)").pack()

    def get_statistics(self):
        # Получить данные из БД
        books = self.db.fetch_all_books()
        movies = self.db.fetch_all_movies()
        
        books_read = sum(1 for b in books if b[7] == "Прочитано")
        total_books = len(books)
        books_percent = (books_read / total_books) * 100 if total_books else 0
        
        movies_watched = sum(1 for m in movies if m[7] == "Просмотрено")
        total_movies = len(movies)
        movies_percent = (movies_watched / total_movies) * 100 if total_movies else 0
        
        return {
            'books_read': books_read,
            'total_books': total_books,
            'books_percent': books_percent,
            'movies_watched': movies_watched,
            'total_movies': total_movies,
            'movies_percent': movies_percent
        }

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        books = self.db.fetch_all_books()
        for book in books:
            self.tree.insert("", "end", text=book[0], values=("Книга", book[1], book[2], book[3], book[7], f"{book[8]*100:.0f}%"))
        movies = self.db.fetch_all_movies()  # Добавьте метод fetch_all_movies в database.py
        for movie in movies:
            self.tree.insert("", "end", text=movie[0], values=("Фильм", movie[1], movie[2], movie[3], movie[7], f"{movie[8]*100:.0f}%"))
        # Добавить фильмы и отобразить в treeview...

    def apply_filter(self):
        pass
        # Логика фильтрации по статусу

    def open_add_book(self):
        AddBookWindow(self.root, self.db, parent=self)

    def open_add_movie(self):
        self.tree.delete(*self.tree.get_children())
        books = self.db.fetch_all_books()
        for book in books:
            self.tree.insert("", "end", values=("Фильм", book[1], book[2], book[3], book[7]))

    def edit_element(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        item_values = self.tree.item(selected_item)['values']
        element_id = self.tree.item(selected_item)['text']
        if item_values[0] == "Книга":
            book_data = self.db.get_book_by_id(element_id)
            if book_data:
                AddBookWindow(self.root, self.db, parent=self, book_data=book_data)
        elif item_values[0] == "Фильм":
            movie_data = self.db.get_movie_by_id(element_id)
            if movie_data:
                AddMovieWindow(self.root, self.db, parent=self, movie_data=movie_data)

    def open_add_movie(self):
        AddMovieWindow(self.root, self.db, parent=self)