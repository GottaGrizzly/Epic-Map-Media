class AddForm:
    def __init__(self, root, type_):
        self.root = tk.Toplevel(root)
        self.type_ = type_
        self.create_ui()

    def create_ui(self):
        # Создание полей ввода
        # ...
        
        submit_btn = ttk.Button(self.root, text="Добавить", command=self.submit)
        submit_btn.pack(pady=10)

    def submit(self):
        # Обработка данных и сохранение в БД
        if self.type_ == 'book':
            self.db.insert_book(data)
        # ...