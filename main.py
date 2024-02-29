import sys

from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton, QVBoxLayout


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
        model = QSqlTableModel(self, db)
        model.setTable('coffee')
        model.select()
        model.setEditStrategy(
            QSqlTableModel.OnManualSubmit)  # требует явного вызова submitAll() для применения изменений.

        # Для отображения данных на виджете
        # свяжем его и нашу модель данных
        self.Coffe_table.setModel(model)

        self.setWindowTitle('Эспрессо')
        self.change_button.clicked.connect(self.open_additional_form)

    def open_additional_form(self):
        main_form.setEnabled(False)  # Делаем основную форму неактивной
        self.additional_form = AdditionalForm(main_form)
        self.additional_form.show()


class AdditionalForm(QMainWindow):
    def __init__(self, main_form):
        super().__init__()
        self.main_form = main_form  # Сохраняем ссылку на основную форму
        self.setWindowTitle('Дополнительная форма')
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()
        button_close = QPushButton('Закрыть', self)
        button_close.clicked.connect(self.close_additional_form)
        layout.addWidget(button_close)
        self.setLayout(layout)

    def close_additional_form(self):
        self.close()

    def closeEvent(self, event):
        self.main_form.setEnabled(True)   # Восстанавливаем активность основной формы


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_form = Cappuchino()
    main_form.show()
    sys.exit(app.exec())
