import pandas as pd
import mysql.connector
import json
import datetime
import ctypes, sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, \
    QPushButton, QMainWindow, QLabel
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QLabel, QPushButton, QPlainTextEdit, QApplication, QCheckBox, QMainWindow, QWidget,
                             QVBoxLayout, QTabWidget)
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

with open('config_path.json', encoding="utf8") as conf:
    config = json.load(conf)

with open(config[0]['config_db']+'/config_db.json', encoding="utf8") as save:
    json_db = json.load(save)

# Подключение к БД
conn = mysql.connector.connect(user=json_db[0]['login'], password=json_db[0]['password'], host=json_db[0]['host'],
                                   database=json_db[0]['name_db'])
cursor = conn.cursor(buffered=True)

class Ui_Login(QtWidgets.QWidget):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(496, 265)
        self.uname_lineEdit = QLineEdit(Login)
        self.uname_lineEdit.setGeometry(QRect(230, 110, 113, 20))
        self.uname_lineEdit.setObjectName("uname_lineEdit")
        self.pass_lineEdit = QLineEdit(Login)
        self.pass_lineEdit.setGeometry(QRect(230, 150, 113, 20))
        self.pass_lineEdit.setObjectName("pass_lineEdit")
        self.pass_lineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.login_btn = QPushButton(Login)
        self.login_btn.setGeometry(QRect(230, 200, 51, 23))
        self.login_btn.setObjectName("login_btn")
        self.label = QLabel(Login)
        self.label.setGeometry(QRect(190, 10, 211, 51))
        self.label.setObjectName("label")
        self.label1 = QLabel(Login)
        self.label1.setGeometry(QRect(190, 10, 211, 51))
        self.label1.setObjectName("label1")
        hl = QHBoxLayout()
        hl.addWidget(self.label)
        hl.addWidget(self.uname_lineEdit)
        hl1 = QHBoxLayout()
        hl1.addWidget(self.label1)
        hl1.addWidget(self.pass_lineEdit)
        hl2 = QHBoxLayout()
        hl2.addWidget(self.login_btn)
        vl = QVBoxLayout()
        vl.addLayout(hl)
        vl.addLayout(hl1)
        vl.addLayout(hl2)
        self.setLayout(vl)
        self.retranslateUi(Login)
        QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Вход в систему"))
        self.login_btn.setText(_translate("Login", "Войти"))
        self.label.setText(_translate("Login", "Логин"))
        self.label1.setText(_translate("Login", "Пароль"))


class Login(QtWidgets.QDialog, Ui_Login):
    # основная логика окна
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setupUi(self)
        self.login_btn.clicked.connect(self.loginCheck)

    # показать сообщения
    def showMessageBox(self, title, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    # открыть класс главного окна
    def mainWindowShow(self, login):
        self.mainWindow = MainWindow(login)
        self.mainWindow.show()

    # проверка авторизации
    def loginCheck(self):
        username = self.uname_lineEdit.text()
        password = self.pass_lineEdit.text()
        if (not username) or (not password):
            msg = QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return
        sel_user = 'SELECT * FROM `users` WHERE `login` = %s AND `password` = %s'
        user = []
        user.append(username)
        user.append(password)
        cursor.execute(sel_user, user)
        if cursor.fetchone() != None:
            self.mainWindowShow(username)
            self.hide()
        else:
            self.showMessageBox('Внимание!', 'Неправильное имя пользователя или пароль.')


class Ui_MainWindow(QtWidgets.QWidget):
    # объявление всех кнопок и надписей
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.open_pars = QtWidgets.QPushButton(self.centralwidget)
        self.open_pars.setGeometry(QtCore.QRect(250, 130, 89, 25))
        self.open_pars.setObjectName("open_pars")
        self.open_pars.findChild(QPushButton, 'open_pars')
        self.pars_ = QtWidgets.QPushButton(self.centralwidget)
        self.pars_.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.pars_.setObjectName("pars_")
        self.pars_.findChild(QPushButton, 'pars_')
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_2.setObjectName("label_2")
        self.filename_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.filename_2.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.filename_2.setObjectName("filename_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 2560, 1600))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "АИС Деканат"))
        self.label_2.setText(_translate("MainWindow", "Укажите путь к файлу:"))
        self.open_pars.setText(_translate("MainWindow", "Обзор..."))
        self.pars_.setText(_translate("MainWindow", "Загрузить"))

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, login):
        sel_test = 'SELECT * FROM `users` WHERE `login` = %s'
        l = []
        l.append(login)
        cursor.execute(sel_test, l)
        self.user = cursor.fetchone()
        super().__init__()
        self.setupUi(self)
        self.parser_ = QWidget()
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.addTab(self.parser_, "Загрузка")
        self.parserUi()
        self.open_pars.clicked.connect(self.pars_win)
        self.pars_.clicked.connect(self.parser)

    def parserUi(self):
        hlayout = QHBoxLayout(self)
        self.tabWidget = QTabWidget(self.centralwidget)
        hlayout.addWidget(self.label_2)
        hlayout.addWidget(self.filename_2)
        hlayout.addWidget(self.open_pars)
        vlayout = QVBoxLayout(self)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.pars_)
        self.tabWidget.setTabText(0, "Parser")
        self.parser_.setLayout(vlayout)

    def parser(self):
        df = pd.read_excel(io=self.file_, engine='openpyxl', sheet_name='Лист1')

        # Парс excel
        result = []

        # Парс ЧИСЛИТЕЛЯ
        for i in range(0, len(df['Числитель'].tolist())):
            dates = df['Числитель'].tolist()[i]
            str_start_date = ''
            str_end_date = ''
            for j in range(0, len(dates)):
                if dates[j] != '-' and j < 10:
                    str_start_date += dates[j]
                elif dates[j] != '-' and j > 10:
                    str_end_date += dates[j]
            day = ''
            mouth = ''
            year = ''
            for j in range(0, len(str_start_date)):
                if j < 2 and str_start_date[j] != '.':
                    day+=str_start_date[j]
                elif j > 2 and j < 5 and str_start_date[j] != '.':
                    mouth+=str_start_date[j]
                elif j > 5 and str_start_date[j] != '.':
                    year+=str_start_date[j]
            start_date = datetime.datetime(int(year), int(mouth), int(day))
            day = ''
            mouth = ''
            year = ''
            for j in range(0, len(str_end_date)):
                if j < 2 and str_end_date[j] != '.':
                    day+=str_end_date[j]
                elif j > 2 and j < 5 and str_end_date[j] != '.':
                    mouth+=str_end_date[j]
                elif j > 5 and str_end_date[j] != '.':
                    year+=str_end_date[j]
            end_date = datetime.datetime(int(year), int(mouth), int(day))
            res = pd.date_range(min(start_date, end_date), max(start_date, end_date)).strftime('%Y-%m-%d').tolist()
            for j in range(0, len(res)):
                cursor.execute("SELECT `id` FROM `type_week` WHERE `name` = 'числитель'")
                result.append(cursor.fetchone()[0])
                result.append(res[j])
                add_res = 'INSERT INTO `date_type_week` (`type_week_id`, `date_week`) VALUES (%s, %s)'
                cursor.execute(add_res, result)
                conn.commit()
                result = []

        # Парс ЗНАМЕНАТЕЛЯ
        for i in range(0, len(df['Знаменатель'].tolist())):
            dates = df['Знаменатель'].tolist()[i]
            str_start_date = ''
            str_end_date = ''
            for j in range(0, len(dates)):
                if dates[j] != '-' and j < 10:
                    str_start_date += dates[j]
                elif dates[j] != '-' and j > 10:
                    str_end_date += dates[j]
            day = ''
            mouth = ''
            year = ''
            for j in range(0, len(str_start_date)):
                if j < 2 and str_start_date[j] != '.':
                    day += str_start_date[j]
                elif j > 2 and j < 5 and str_start_date[j] != '.':
                    mouth += str_start_date[j]
                elif j > 5 and str_start_date[j] != '.':
                    year += str_start_date[j]
            start_date = datetime.datetime(int(year), int(mouth), int(day))
            day = ''
            mouth = ''
            year = ''
            for j in range(0, len(str_end_date)):
                if j < 2 and str_end_date[j] != '.':
                    day += str_end_date[j]
                elif j > 2 and j < 5 and str_end_date[j] != '.':
                    mouth += str_end_date[j]
                elif j > 5 and str_end_date[j] != '.':
                    year += str_end_date[j]
            end_date = datetime.datetime(int(year), int(mouth), int(day))
            res = pd.date_range(min(start_date, end_date), max(start_date, end_date)).strftime(
                '%Y-%m-%d').tolist()
            for j in range(0, len(res)):
                cursor.execute("SELECT `id` FROM `type_week` WHERE `name` = 'знаменатель'")
                result.append(cursor.fetchone()[0])
                result.append(res[j])
                add_res = 'INSERT INTO `date_type_week` (`type_week_id`, `date_week`) VALUES (%s, %s)'
                cursor.execute(add_res, result)
                conn.commit()
                result = []

    def pars_win(self):
        self.open_pars.hide()
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './', '(*.xls *.xlsx)')
        if fname:
            self.filename_2.setText(fname)
            self.file_ = str(fname)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    splash = QtWidgets.QSplashScreen()
    splash.setPixmap(QtGui.QPixmap('images/splash.jpg'))
    splash.show()
    splash.showMessage('<h1 style="color:#ffffff;">Добро пожаловать в АИС Деканат (beta)</h1>',
                       QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft, QtCore.Qt.white)
    QtCore.QThread.msleep(5000)
    w = Login()
    w.show()
    splash.hide()
    sys.exit(app.exec_())