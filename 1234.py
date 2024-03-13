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
        self.coords = 37.526286, 55.831216
        # максимальный размер 650х450
        self.size = ('650', '450')
        self.scale = 0.002, 0.002
        self.get_map()

    def get_map(self):
        request = f"http://static-maps.yandex.ru/1.x/?ll=" \
                  f"{','.join([str(x) for x in self.coords])}" \
                  f"&size={','.join(self.size)}&spn={','.join([str(x) for x in self.scale])}&l=map"
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
        up = 16777235
        down = 16777237
        left = 16777234
        right = 16777236
        if key == page_up:
            if self.scale[0] < 50:
                self.scale = self.scale[0] + 0.002, self.scale[1] + 0.002
        elif key == page_down:
            if self.scale[0] > 0.002:
                self.scale = self.scale[0] - 0.002, self.scale[1] - 0.002
        elif key == up:
            self.coords = self.coords[0], self.coords[1] + self.scale[1] / 2
        elif key == down:
            self.coords = self.coords[0], self.coords[1] - self.scale[1] / 2
        elif key == left:
            self.coords = self.coords[0] - self.scale[0] / 2, self.coords[1]
        elif key == right:
            self.coords = self.coords[0] + self.scale[0] / 2, self.coords[1]
        self.get_map()


app = QApplication(sys.argv)
ex = ApiWindow()
ex.show()
sys.exit(app.exec_())
