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
        self.setWindowTitle('Большая задача по api - 1')
        self.kartinka.setPixmap(QtGui.QPixmap('image.png'))


# Моя обитель находится по следующим координатам
coordinates = map(str, (55.831216, 37.526286)[::-1])
# максимальный размер 650х450
size = map(str, (650, 450))
# Изменяется в пределах 0 - 21
scale = 15

apikey = "40d1649f-0493-4b70-98ba-98533de7710b"
request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(coordinates)}&size={','.join(size)}&z={scale}&l=map"

response = requests.get(request)

if response.status_code == 200:
    with open('image.png', 'wb') as file:
        file.write(response.content)
    app = QApplication(sys.argv)
    ex = ApiWindow()
    ex.show()
    sys.exit(app.exec_())
else:
    print('Ошибка при получении изображения.')
