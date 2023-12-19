import sys
from PyQt6 import QtWidgets, uic
import client
import openpyxl
from time import sleep

tab1_ui, _ = uic.loadUiType("ui/auth_w.ui")
tab2_ui, _ = uic.loadUiType("ui/select_table.ui")
tab3_ui, _ = uic.loadUiType("ui/table.ui")
tab4_ui, _ = uic.loadUiType("ui/table_add.ui")
tab5_ui, _ = uic.loadUiType("ui/cook_w.ui")


class Tab1(QtWidgets.QMainWindow, tab1_ui):
    """Класс виджета авторизации"""
    def __init__(self, parent=None):
        super(Tab1, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(login)


class Tab2(QtWidgets.QMainWindow, tab2_ui):
    """Класс виджета с выбором стола для официанта"""
    def __init__(self, parent=None):
        super(Tab2, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_1.clicked.connect(lambda: select_table(1))
        self.pushButton_2.clicked.connect(lambda: select_table(2))
        self.pushButton_3.clicked.connect(lambda: select_table(3))
        self.pushButton_4.clicked.connect(lambda: select_table(4))
        self.pushButton_5.clicked.connect(lambda: select_table(5))
        self.pushButton_6.clicked.connect(lambda: select_table(6))
        self.pushButton_7.clicked.connect(lambda: select_table(7))
        self.pushButton_8.clicked.connect(lambda: select_table(8))
        self.pushButton_9.clicked.connect(lambda: select_table(9))
        self.pushButton_10.clicked.connect(lambda: select_table(10))
        self.pushButton_11.clicked.connect(lambda: select_table(11))
        self.pushButton_12.clicked.connect(lambda: select_table(12))
        self.backButton.clicked.connect(logout)


class Tab3(QtWidgets.QMainWindow, tab3_ui):
    """Класс виджета выбранного стола для официанта"""
    n = 0
    def __init__(self, parent=None):
        super(Tab3, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_page)
        self.pushButton_2.clicked.connect(remove_dishes)
        self.pushButton_3.clicked.connect(checkout)
        self.backButton.clicked.connect(back_to_tables)
    def add_page(self):
        """Функция для перехода на виджет добавления блюда"""
        r = client.get_dishes_list()
        tab4.curr_r = r
        tab4.comboBox.clear()
        tab4.comboBox.addItems([i[0] for i in r])
        w.setCurrentWidget(tab4)  


class Tab4(QtWidgets.QMainWindow, tab4_ui):
    """Класс виджета добавления блюда на стол"""
    curr_r = []
    def __init__(self, parent=None):
        super(Tab4, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_confirm)   
    def add_confirm(self):
        """Функция добавления блюда на стол. Считывает имя и блюдо из полей в виджете"""
        name = self.lineEdit.text()
        dish = self.comboBox.currentText()
        if name == '':
            w.setCurrentWidget(tab3)
            return
        for i in self.curr_r:
            if i[0] == dish:
                r = [name, dish, i[4]]
                client.add_dish_to_table(r, tab3.n)
                break
        refresh_dishes()
        w.setCurrentWidget(tab3)
        self.lineEdit.setText('')


class Tab5(QtWidgets.QMainWindow, tab5_ui):
    """Класс виджета меню для повора"""
    def __init__(self, parent=None):
        super(Tab5, self).__init__(parent)
        self.setupUi(self)
        self.backButton.clicked.connect(logout)
        self.pushButton.clicked.connect(add_dish_to_sl)
        self.pushButton_2.clicked.connect(remove_dish_from_sl)
        self.pushButton_3.clicked.connect(add_product_to_sl)


def login():
    """Функция входа по коду работника. Код считывается из поля на форме авторизации. Проверка происходит на сервере"""
    tab1.label_2.setText('')
    try:
        r = client.connect(tab1.lineEdit.text())
        if r == 'WAITER':
            w.setCurrentWidget(tab2)
        if r == 'COOK':
            w.setCurrentWidget(tab5)
            show_dishes()
        if r == 'NOWORKER':
            tab1.label_2.setText('Ошибка. Неправильный код.')
    except: 
        tab1.label_2.setText('Ошибка. Проблема c соединением.')

    
def logout():
    """Функция отключения и перехода в виджет авторизации"""
    w.setCurrentWidget(tab1)
    client.disconnect()


def refresh_dishes():
    """Функция для обновления отображения списка блюд на виджете стола"""
    tab3.listWidget.clear()
    data = client.get_table_data(tab3.n)
    for i in data:
        tab3.listWidget.addItem('\t'.join(i))


def select_table(n):
    "Функция настройки виджета стола для выбранного стола"
    hlabel = f'Стол# {n}'
    tab3.label.setText(hlabel)
    tab3.n = n
    refresh_dishes()
    w.setCurrentWidget(tab3)


def back_to_tables():
    """Функция для возвращения к списку столов"""
    w.setCurrentWidget(tab2)
    tab3.listWidget.clear()


def remove_dishes():
    """Функция для удаления блюда со стола"""
    dishes = tab3.listWidget.selectedItems()
    D = (dishes[0]).text().split('\t')
    client.remove_dish_from_table(D, tab3.n)
    refresh_dishes()


def show_dishes():
    """Функция для добавления списка блюд в комбобокс виджета добавления блюда на стол"""
    tab5.comboBox.clear()
    r = client.get_all_dishes_list()
    dishes = [(i[0] + '|в стоп-листе:'+ i[3]) for i in r]
    tab5.comboBox.addItems(dishes)


def add_dish_to_sl():
    """Функция добавления блюда в стоп-лист"""
    d = tab5.comboBox.currentText().split('|')[0]
    N = tab5.comboBox.currentIndex()
    client.dish_to_sl(d)
    
    sleep(0.1)
    client.disconnect()
    client.connect(tab1.lineEdit.text())
    show_dishes()
    tab5.comboBox.setCurrentIndex(N)


def remove_dish_from_sl():
    """Функция удаления блюда из стоп-листа"""
    d = tab5.comboBox.currentText().split('|')[0]
    N = tab5.comboBox.currentIndex()
    client.dish_from_sl(d)

    sleep(0.1)
    client.disconnect()
    client.connect(tab1.lineEdit.text())
    show_dishes()
    tab5.comboBox.setCurrentIndex(N)


def add_product_to_sl():
    """Функция добавления блюд в стоп-лист по указанному продукту"""
    product = tab5.lineEdit.text().lower()
    tab5.lineEdit.setText('')
    if product != '':
        N = tab5.comboBox.currentIndex()
        client.product_to_sl(product)

        sleep(0.1)
        client.disconnect()
        client.connect(tab1.lineEdit.text())
        show_dishes()
        tab5.comboBox.setCurrentIndex(N)


def checkout():
    """Функция создания чека"""
    data = client.get_table_data(tab3.n)

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    sheet.append(['Имя гостя', 'Блюдо', 'Цена'])
    sum = 0
    for row in data:
        sheet.append(row)
        sum+= int(row[2])
    sheet.append(['', '', 'Итого'])
    sheet.append(['', '', sum])

    workbook.save(f'check_table{tab3.n}.xlsx')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QStackedWidget()

    tab1 = Tab1()
    tab2 = Tab2()
    tab3 = Tab3()
    tab4 = Tab4()
    tab5 = Tab5()
    
    w.addWidget(tab1)
    w.addWidget(tab2)
    w.addWidget(tab3)
    w.addWidget(tab4)
    w.addWidget(tab5)

    w.show()
    sys.exit(app.exec())