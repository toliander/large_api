import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem


class Cappuchino(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('coffee.sqlite')
        # откроем подключение
        db.open()

        # Создадим объект QSqlTableModel,
        # зададим таблицу, с которой он будет работать,
        #  и выберем все данные
        self.model = QSqlTableModel(self, db)
        self.model.setTable('coffee')
        self.model.select()
        self.model.setEditStrategy(
            QSqlTableModel.OnManualSubmit)  # требует явного вызова submitAll() для применения изменений.

        # Для отображения данных на виджете
        # свяжем его и нашу модель данных
        self.Coffe_table.setModel(self.model)
        self.setWindowTitle('Эспрессо')
        self.change_button.clicked.connect(self.open_additional_form)

        # кликабельный ряд
        self.Coffe_table.clicked.connect(self.on_row_clicked)

    def update_table(self):
        self.model.select()

    def on_row_clicked(self, index):
        row = index.row()
        print(f"Clicked on row {row}")

    def open_additional_form(self):
        main_form.setEnabled(False)  # Делаем основную форму неактивной
        self.additional_form = AdditionalForm(main_form)
        self.additional_form.show()


class AdditionalForm(QMainWindow):
    def __init__(self, main_form):
        super().__init__()
        self.main_form = main_form  # Сохраняем ссылку на основную форму
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.setWindowTitle('Дополнительная форма')
        self.show_button.clicked.connect(self.get_id)
        self.accept_button.clicked.connect(self.save_results)
        self.make_button.clicked.connect(self.push_new)
        self.con = sqlite3.connect("coffee.sqlite")
        self.modified = {}
        self.new = {}
        self.titles = None
        self.id_redo = None
        self.edit_table.itemChanged.connect(self.item_changed)
        self.insert_table.itemChanged.connect(self.new_changed)
        self.refresh_new()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE coffee SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += f"WHERE id = {self.id_redo}"
            cur.execute(que)
            self.con.commit()
            self.modified.clear()
            self.main_form.update_table()

    def get_id(self):
        id = self.id_edit.text()
        self.id_redo = id
        cur = self.con.cursor()
        result = cur.execute(f"SELECT * FROM coffee WHERE id={id}").fetchall()
        self.titles = [description[0] for description in cur.description]
        if result:  # В случае если запрос успешный заносим данные
            self.edit_table.setRowCount(len(result))
            self.edit_table.setColumnCount(len(result[0]))
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.edit_table.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}  # Обнуляем поле для добавления в базу

    def refresh_new(self):
        self.insert_table.setRowCount(1)
        self.insert_table.setColumnCount(7)

    def push_new(self):
        if len(self.new.keys()) == 7:
            cur = self.con.cursor()
            print(self.new.keys())
            que = "INSERT into coffee \n"
            que += '(' + ', '.join(self.new.keys()) + ')\n'
            que += "Values (" + ', '.join(["'" + x + "'" for x in self.new.values()]) + ')'
            print(que)
            cur.execute(que)
            self.con.commit()
            self.new.clear()
            self.main_form.update_table()

    def new_changed(self, item):
        # Если значение в ячейке было изменено,
        # то в словарь записывается пара: название поля, новое значение
        tablenames = ['ID', 'sort_name', 'roast_degree', 'ground_or_whole',
                      'flavor_description', 'price', 'package_volume']
        self.new[tablenames[item.column()]] = item.text()

    def item_changed(self, item):
        # Если значение в ячейке было изменено,
        # то в словарь записывается пара: название поля, новое значение
        self.modified[self.titles[item.column()]] = item.text()

    def closeEvent(self, event):
        self.main_form.setEnabled(True)  # Восстанавливаем активность основной формы
        self.con.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_form = Cappuchino()
    main_form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
