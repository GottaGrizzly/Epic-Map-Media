# gui/add_window.py
import os
import tkinter as tk
from tkinter import Image, ttk
from tkinter import messagebox
from tkinter import filedialog

class AddBookWindow:
    def __init__(self, root, db, parent=None, book_data=None):
        self.root = tk.Toplevel(root)
        self.db = db
        self.parent = parent
        self.book_data = book_data
        self.cover_path = ""
        self.create_ui()

        if book_data:
            self.fill_form()

    def create_ui(self):
        self.root.title("Добавить/Редактировать книгу")
        self.root.geometry("500x600")

        # Основные поля
        form_frame = ttk.Frame(self.root, padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Название
        ttk.Label(form_frame, text="Название*:").grid(row=0, column=0, sticky=tk.W)
        self.title = ttk.Entry(form_frame, width=40)
        self.title.grid(row=0, column=1, pady=5)

        # Автор
        ttk.Label(form_frame, text="Автор*:").grid(row=1, column=0, sticky=tk.W)
        self.author = ttk.Entry(form_frame, width=40)
        self.author.grid(row=1, column=1, pady=5)

        # Год
        ttk.Label(form_frame, text="Год издания:").grid(row=2, column=0, sticky=tk.W)
        self.year = ttk.Entry(form_frame, width=10)
        self.year.grid(row=2, column=1, sticky=tk.W, pady=5)

        # Жанр
        ttk.Label(form_frame, text="Жанр:").grid(row=3, column=0, sticky=tk.W)
        self.genre = ttk.Entry(form_frame, width=30)
        self.genre.grid(row=3, column=1, sticky=tk.W, pady=5)

        # Статус
        ttk.Label(form_frame, text="Статус:").grid(row=4, column=0, sticky=tk.W)
        self.status = ttk.Combobox(form_frame, values=["Не прочитано", "В процессе", "Прочитано"], width=20)
        self.status.grid(row=4, column=1, sticky=tk.W, pady=5)
        self.status.set("Не прочитано")

        # Прогресс
        ttk.Label(form_frame, text="Прогресс (%):").grid(row=5, column=0, sticky=tk.W)
        self.progress = ttk.Scale(form_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=200)
        self.progress.grid(row=5, column=1, sticky=tk.W, pady=5)
        self.progress.set(0)

        # Обложка
        ttk.Label(form_frame, text="Обложка:").grid(row=6, column=0, sticky=tk.W)
        self.cover_preview = ttk.Label(form_frame)
        self.cover_preview.grid(row=6, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(form_frame, text="Выбрать обложку", command=self.select_cover).grid(
            row=7, column=1, sticky=tk.W, pady=5)

        # Описание
        ttk.Label(form_frame, text="Описание:").grid(row=8, column=0, sticky=tk.NW)
        self.description = tk.Text(form_frame, height=5, width=40)
        self.description.grid(row=8, column=1, pady=5)

        # Заметки
        ttk.Label(form_frame, text="Заметки:").grid(row=9, column=0, sticky=tk.NW)
        self.notes = tk.Text(form_frame, height=5, width=40)
        self.notes.grid(row=9, column=1, pady=5)

        # Рецензия
        ttk.Label(form_frame, text="Рецензия:").grid(row=10, column=0, sticky=tk.NW)
        self.review = tk.Text(form_frame, height=5, width=40)
        self.review.grid(row=10, column=1, pady=5)

        # Кнопки
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Сохранить", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=self.root.destroy).pack(side=tk.LEFT)

    def fill_form(self):
        """Заполнение формы данными для редактирования"""
        self.title.delete(0, tk.END)
        self.title.insert(0, self.book_data[1])
        
        self.author.delete(0, tk.END)
        self.author.insert(0, self.book_data[2])
        
        if self.book_data[3]:
            self.year.delete(0, tk.END)
            self.year.insert(0, str(self.book_data[3]))
        
        if self.book_data[4]:
            self.genre.delete(0, tk.END)
            self.genre.insert(0, self.book_data[4])
        
        if self.book_data[7]:
            self.status.set(self.book_data[7])
        
        if self.book_data[8]:
            self.progress.set(self.book_data[8])
        
        if self.book_data[5]:  # cover_path
            self.cover_path = self.book_data[5]
            self.show_cover_preview()

            self.description.delete("1.0", tk.END)
        if self.book_data[6]:
            self.description.insert(tk.END, self.book_data[6])
        
        self.notes.delete("1.0", tk.END)
        if self.book_data[9]:
            self.notes.insert(tk.END, self.book_data[9])
        
        self.review.delete("1.0", tk.END)
        if self.book_data[10]:
            self.review.insert(tk.END, self.book_data[10])

    def select_cover(self):
        """Выбор файла обложки"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Изображения", "*.jpg *.jpeg *.png *.gif")]
        )
        if file_path:
            self.cover_path = file_path
            self.show_cover_preview()

    def show_cover_preview(self):
        """Показ превью обложки"""
        try:
            image = Image.open(self.cover_path)
            image.thumbnail((100, 150))
            photo = ImageTk.PhotoImage(image)
            
            self.cover_preview.configure(image=photo)
            self.cover_preview.image = photo  # Сохраняем ссылку
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")

    def validate(self):
        """Проверка обязательных полей"""
        if not self.title.get().strip():
            messagebox.showwarning("Ошибка", "Введите название книги!")
            return False
            
        if not self.author.get().strip():
            messagebox.showwarning("Ошибка", "Введите автора книги!")
            return False
            
        if self.year.get() and not self.year.get().isdigit():
            messagebox.showwarning("Ошибка", "Год должен быть числом!")
            return False
            
        return True
    
    def save(self):
        if self.parent:  # Передайте ссылку на MainWindow
            self.parent.load_data()
        """Сохранение данных в БД"""
        if not self.validate():
            return
        
        try:
            # Подготовка данных
            title = self.title.get().strip()
            author = self.author.get().strip()
            year = int(self.year.get()) if self.year.get() else None
            genre = self.genre.get().strip()
            status = self.status.get()
            progress = float(self.progress.get())
            description = self.description.get("1.0", tk.END).strip()
            notes = self.notes.get("1.0", tk.END).strip()
            review = self.review.get("1.0", tk.END).strip()

            # Сохранение обложки (копируем в папку covers)
            cover_db_path = None
            if self.cover_path:
                # Создаем папку covers, если ее нет
                if not os.path.exists("covers"):
                    os.makedirs("covers")
                
                # Генерируем уникальное имя файла
                filename = f"{hash(title + author)}.jpg"
                cover_db_path = os.path.join("covers", filename)
                
                # Сохраняем копию обложки
                image = Image.open(self.cover_path)
                image.save(cover_db_path)

                # Сохранение в БД
            if self.book_data:  # Редактирование
                book_id = self.book_data[0]
                self.db.update_book(book_id, title, author, year, genre, cover_db_path,
                                  description, status, progress, notes, review)
                messagebox.showinfo("Успех", "Книга успешно обновлена!")
            else:  # Добавление
                self.db.insert_book(title, author, year, genre, cover_db_path,
                                  description, status, progress, notes, review)
                messagebox.showinfo("Успех", "Книга успешно добавлена!")

            if self.parent:
                self.parent.load_data()

            self.root.destroy()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}")
        finally:
            self.root.destroy()

class AddElementWindow:
    def __init__(self, root, element_type, data=None):
        self.root = tk.Toplevel(root)
        self.element_type = element_type
        self.data = data  # Для редактирования существующей записи
        self.create_ui()

    def create_ui(self):
        # Основные поля
        ttk.Label(self.root, text="Название:").grid(row=0, column=0)
        self.title_entry = ttk.Entry(self.root)
        self.title_entry.grid(row=0, column=1)

        ttk.Label(self.root, text="Автор/Режиссер:").grid(row=1, column=0)
        self.author_entry = ttk.Entry(self.root)
        self.author_entry.grid(row=1, column=1)

        # Кнопка сохранения
        save_btn = ttk.Button(self.root, text="Сохранить", command=self.save)
        save_btn.grid(row=5, columnspan=2)

        # Статус
        ttk.Label(self.root, text="Статус:").grid(row=3, column=0)
        self.status_var = tk.StringVar()
        statuses = ["Прочитано", "В процессе", "Не прочитано", "Просмотрено"]
        ttk.Combobox(self.root, textvariable=self.status_var, values=statuses).grid(row=3, column=1)

        # Прогресс
        ttk.Label(self.root, text="Прогресс:").grid(row=4, column=0)
        self.progress_scale = ttk.Scale(self.root, from_=0, to=1, orient=tk.HORIZONTAL)
        self.progress_scale.grid(row=4, column=1)

    def save(self):
        # Получение данных из полей
        title = self.title_entry.get()
        author = self.author_entry.get()

        if self.data:
            # Редактирование существующей записи
            self.master.db.update_element(self.element_type, self.data[0], title, author, ...)
        else:
            # Добавление новой записи
            self.master.db.insert_element(self.element_type, title, author, ...)

        self.root.destroy()

class AddMovieWindow:
    def __init__(self, root, db, parent=None, movie_data=None):
        self.root = tk.Toplevel(root)
        self.db = db
        self.parent = parent
        self.movie_data = movie_data
        self.cover_path = ""
        self.create_ui()
        if movie_data:
            self.fill_form()

    def create_ui(self):
        self.root.title("Добавить/Редактировать фильм")
        self.root.geometry("500x600")
        form_frame = ttk.Frame(self.root, padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Название
        ttk.Label(form_frame, text="Название*:").grid(row=0, column=0, sticky=tk.W)
        self.title = ttk.Entry(form_frame, width=40)
        self.title.grid(row=0, column=1, pady=5)

        # Режиссёр
        ttk.Label(form_frame, text="Режиссёр*:").grid(row=1, column=0, sticky=tk.W)
        self.director = ttk.Entry(form_frame, width=40)
        self.director.grid(row=1, column=1, pady=5)

        # Год
        ttk.Label(form_frame, text="Год выпуска:").grid(row=2, column=0, sticky=tk.W)
        self.year = ttk.Entry(form_frame, width=10)
        self.year.grid(row=2, column=1, sticky=tk.W, pady=5)

        # Жанр
        ttk.Label(form_frame, text="Жанр:").grid(row=3, column=0, sticky=tk.W)
        self.genre = ttk.Entry(form_frame, width=30)
        self.genre.grid(row=3, column=1, sticky=tk.W, pady=5)

        # Статус
        ttk.Label(form_frame, text="Статус:").grid(row=4, column=0, sticky=tk.W)
        self.status = ttk.Combobox(form_frame, values=["Не просмотрено", "Смотрю", "Просмотрено"], width=20)
        self.status.grid(row=4, column=1, sticky=tk.W, pady=5)
        self.status.set("Не просмотрено")

        # Прогресс
        ttk.Label(form_frame, text="Прогресс (%):").grid(row=5, column=0, sticky=tk.W)
        self.progress = ttk.Scale(form_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=200)
        self.progress.grid(row=5, column=1, sticky=tk.W, pady=5)
        self.progress.set(0)

        # Обложка
        ttk.Label(form_frame, text="Обложка:").grid(row=6, column=0, sticky=tk.W)
        self.cover_preview = ttk.Label(form_frame)
        self.cover_preview.grid(row=6, column=1, sticky=tk.W, pady=5)
        ttk.Button(form_frame, text="Выбрать обложку", command=self.select_cover).grid(
            row=7, column=1, sticky=tk.W, pady=5)

        # Описание
        ttk.Label(form_frame, text="Описание:").grid(row=8, column=0, sticky=tk.NW)
        self.description = tk.Text(form_frame, height=5, width=40)
        self.description.grid(row=8, column=1, pady=5)

        # Заметки
        ttk.Label(form_frame, text="Заметки:").grid(row=9, column=0, sticky=tk.NW)
        self.notes = tk.Text(form_frame, height=5, width=40)
        self.notes.grid(row=9, column=1, pady=5)

        # Кнопки
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Сохранить", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=self.root.destroy).pack(side=tk.LEFT)

    def fill_form(self):
        """Заполнение формы данными для редактирования"""
        self.title.delete(0, tk.END)
        self.title.insert(0, self.movie_data[1])
        self.director.delete(0, tk.END)
        self.director.insert(0, self.movie_data[2])
        if self.movie_data[3]:
            self.year.delete(0, tk.END)
            self.year.insert(0, str(self.movie_data[3]))
        if self.movie_data[4]:
            self.genre.delete(0, tk.END)
            self.genre.insert(0, self.movie_data[4])
        if self.movie_data[7]:
            self.status.set(self.movie_data[7])
        if self.movie_data[8]:
            self.progress.set(self.movie_data[8])
        if self.movie_data[5]:  # cover_path
            self.cover_path = self.movie_data[5]
            self.show_cover_preview()
        self.description.delete("1.0", tk.END)
        if self.movie_data[6]:
            self.description.insert(tk.END, self.movie_data[6])
        self.notes.delete("1.0", tk.END)
        if self.movie_data[9]:
            self.notes.insert(tk.END, self.movie_data[9])

    def select_cover(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Изображения", "*.jpg *.jpeg *.png *.gif")]
        )
        if file_path:
            self.cover_path = file_path
            self.show_cover_preview()

    def show_cover_preview(self):
        try:
            image = Image.open(self.cover_path)
            image.thumbnail((100, 150))
            photo = ImageTk.PhotoImage(image)
            self.cover_preview.configure(image=photo)
            self.cover_preview.image = photo
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")

    def validate(self):
        if not self.title.get().strip():
            messagebox.showwarning("Ошибка", "Введите название фильма!")
            return False
        if not self.director.get().strip():
            messagebox.showwarning("Ошибка", "Введите режиссёра фильма!")
            return False
        if self.year.get() and not self.year.get().isdigit():
            messagebox.showwarning("Ошибка", "Год должен быть числом!")
            return False
        return True
    
    def save(self):
        if not self.validate():
            return
        try:
            title = self.title.get().strip()
            director = self.director.get().strip()
            year = int(self.year.get()) if self.year.get() else None
            genre = self.genre.get().strip()
            status = self.status.get()
            progress = float(self.progress.get())
            description = self.description.get("1.0", tk.END).strip()
            notes = self.notes.get("1.0", tk.END).strip()

            cover_db_path = None
            if self.cover_path:
                if not os.path.exists("covers"):
                    os.makedirs("covers")
                filename = f"{hash(title + director)}.jpg"
                cover_db_path = os.path.join("covers", filename)
                image = Image.open(self.cover_path)
                image.save(cover_db_path)

            if self.movie_data:  # Редактирование
                movie_id = self.movie_data[0]
                self.db.update_movie(movie_id, title, director, year, genre, cover_db_path,
                                    description, status, progress, notes)
                messagebox.showinfo("Успех", "Фильм успешно обновлён!")
            else:  # Добавление
                self.db.insert_movie(title, director, year, genre, cover_db_path,
                                    description, status, progress, notes)
                messagebox.showinfo("Успех", "Фильм успешно добавлен!")

            self.root.destroy()
            if self.parent:
                self.parent.load_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}")