import requests
import sys
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow


class ApiWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Большая задача по api - 2')
        # Моя обитель находится по следующим координатам
        self.coords = ('55.831216', '37.526286')[::-1]
        # максимальный размер 650х450
        self.size = ('650', '450')
        # Изменяется в пределах 0 - 21
        self.scale = 15
        self.get_map()

    def get_map(self):
        request = f"http://static-maps.yandex.ru/1.x/?ll=" \
                  f"{','.join(self.coords)}&size={','.join(self.size)}&z={self.scale}&l=map"
        response = requests.get(request)
        if response.status_code == 200:
            with open('image.png', 'wb') as file:
                file.write(response.content)
            self.kartinka.setPixmap(QtGui.QPixmap('image.png'))
        else:
            self.kartinka.setText('Ошибка получения изображения')

    def keyPressEvent(self, event):
        key = event.key()
        page_up = 16777238
        page_down = 16777239
        if key == page_up:
            if self.scale < 21:
                self.scale += 1
        elif key == page_down:
            if self.scale > 0:
                self.scale -= 1
        self.get_map()


app = QApplication(sys.argv)
ex = ApiWindow()
ex.show()
sys.exit(app.exec_())
