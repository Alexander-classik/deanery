import pandas as pd
import mysql.connector
import json
import datetime
import ctypes, sys
import os.path
import openpyxl
from PyQt5 import QtCore, QtGui, QtWidgets
from aspose.cells import Workbook, SaveFormat, FileFormatType
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


# class Ui_AutoReserveCopy(QtWidgets.QWidget):
#     def setupUi(self, AutoReserveCopy):
#         super(Ui_AutoReserveCopy, self).__init__()
#         AutoReserveCopy.setObjectName("AutoReserveCopy")
#         AutoReserveCopy.resize(570, 375)
#         self.open_folder = QtWidgets.QPushButton(AutoReserveCopy)
#         self.open_folder.setGeometry(QtCore.QRect(250, 130, 89, 25))
#         self.open_folder.setObjectName("open_folder")
#         self.open_folder.findChild(QPushButton, 'open_folder')
#         self.pars_ = QtWidgets.QPushButton(AutoReserveCopy)
#         self.pars_.setGeometry(QtCore.QRect(30, 150, 241, 55))
#         self.pars_.setObjectName("pars_")
#         self.pars_.findChild(QPushButton, 'pars_')
#         self.label_2 = QtWidgets.QLabel(AutoReserveCopy)
#         self.label_2.setGeometry(QtCore.QRect(10, 110, 241, 17))
#         self.label_2.setObjectName("label_2")
#         self.label_1 = QtWidgets.QLabel(AutoReserveCopy)
#         self.label_1.setGeometry(QtCore.QRect(10, 110, 241, 17))
#         self.label_1.setObjectName("label_1")
#         self.filename_2 = QtWidgets.QLineEdit(AutoReserveCopy)
#         self.filename_2.setGeometry(QtCore.QRect(10, 130, 221, 25))
#         self.filename_2.setObjectName("filename_2")
#         self.num_day_line = QtWidgets.QLineEdit(AutoReserveCopy)
#         self.num_day_line.setGeometry(QtCore.QRect(10, 130, 221, 25))
#         self.num_day_line.setObjectName("num_day_line")
#         self.retranslateUi(AutoReserveCopy)
#         QMetaObject.connectSlotsByName(AutoReserveCopy)
#
#     def retranslateUi(self, AutoReserveCopy):
#         _translate = QCoreApplication.translate
#         AutoReserveCopy.setWindowTitle(_translate("AutoReserveCopy", "Автоматическое резервное копирование"))
#         self.label_2.setText(_translate("AutoReserveCopy", "Выберите папку:"))
#         self.label_1.setText(_translate("AutoReserveCopy", "Количество дней"))
#         self.open_folder.setText(_translate("AutoReserveCopy", "Обзор..."))
#         self.pars_.setText(_translate("AutoReserveCopy", "Загрузить"))
#
#
# class AutoReserveCopy(QtWidgets.QDialog, Ui_AutoReserveCopy):
#     def __init__(self, parent=None):
#         super(AutoReserveCopy, self).__init__(parent)
#         self.setupUi(self)
#         hl = QHBoxLayout()
#         hl.addWidget(self.label_1)
#         hl.addWidget(self.num_day_line)
#         hl1 = QHBoxLayout()
#         hl1.addWidget(self.label_2)
#         hl1.addWidget(self.filename_2)
#         hl1.addWidget(self.open_folder)
#         vl = QVBoxLayout()
#         vl.addLayout(hl)
#         vl.addLayout(hl1)
#         vl.addWidget(self.pars_)
#         self.pars_.clicked.connect(self.write_num_day)
#         self.open_folder.clicked.connect(self.open_win_path)
#
#     def check_save(self):
#         return os.path.exists('reserve_copy_num_day.json')
#
#     def write_num_day(self):
#         if self.check_save():
#             data = [{'num_day': self.num_day_line.text(), 'path': self.path}]
#             with open('reserve_copy_num_day.json', 'w') as save:
#                 json.dump(data, save)
#         else:
#             workbook = Workbook()
#             worksheet = workbook.worksheets[0]
#
#             worksheet.cells.get("A1").put_value("num_day")
#             worksheet.cells.get("B1").put_value("path")
#             worksheet.cells.get("A2").put_value(self.num_day_line.text())
#             worksheet.cells.get("B2").put_value(self.path)
#
#             workbook.save("reserve_copy_num_day.json")
#
#     def open_win_path(self):
#         fname = QtWidgets.QFileDialog.getExistingDirectory(None, "Выбрать папку", ".")
#         if fname:
#             self.filename_2.setText(fname)
#             self.path = fname


class Ui_reserve_copy(QtWidgets.QWidget):
    def setupUi(self, ReserveCopy):
        super(Ui_reserve_copy, self).__init__()
        ReserveCopy.setObjectName("ReserveCopy")
        ReserveCopy.resize(570, 375)
        self.open_pars = QtWidgets.QPushButton(ReserveCopy)
        self.open_pars.setGeometry(QtCore.QRect(250, 130, 89, 25))
        self.open_pars.setObjectName("open_pars")
        self.open_pars.findChild(QPushButton, 'open_pars')
        self.pars_ = QtWidgets.QPushButton(ReserveCopy)
        self.pars_.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.pars_.setObjectName("pars_")
        self.pars_.findChild(QPushButton, 'pars_')
        self.label_2 = QtWidgets.QLabel(ReserveCopy)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_2.setObjectName("label_2")
        self.filename_2 = QtWidgets.QLineEdit(ReserveCopy)
        self.filename_2.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.filename_2.setObjectName("filename_2")
        self.retranslateUi(ReserveCopy)
        QMetaObject.connectSlotsByName(ReserveCopy)

    def retranslateUi(self, ReserveCopy):
        _translate = QCoreApplication.translate
        ReserveCopy.setWindowTitle(_translate("ReserveCopy", "Резервное копирование"))
        self.label_2.setText(_translate("ReserveCopy", "Выберите папку:"))
        self.open_pars.setText(_translate("ReserveCopy", "Обзор..."))
        self.pars_.setText(_translate("ReserveCopy", "Загрузить"))


class ReserveCopy(QtWidgets.QDialog, Ui_reserve_copy):
    def __init__(self, parent=None):
        super(ReserveCopy, self).__init__(parent)
        self.setupUi(self)
        hl = QHBoxLayout()
        hl.addWidget(self.label_2)
        hl.addWidget(self.filename_2)
        hl.addWidget(self.open_pars)
        vl = QVBoxLayout()
        vl.addLayout(hl)
        vl.addWidget(self.pars_)
        self.open_pars.clicked.connect(self.open_win_path)
        self.pars_.clicked.connect(self.reserve_copy)

    def reserve_copy(self):
        cursor.execute('SELECT * FROM `tokens`')
        id_tokens = cursor.fetchall()
        result = []
        for i in range(0, len(id_tokens)):
            name_tokens = 'SELECT ' \
                          '(SELECT `name` FROM `subjects` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `tasks` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `blocks` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `type_tasks` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `teachers` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `groups` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `courses` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `year_enter` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `periods` WHERE `id` = %s) ' \
                          'FROM `tokens`'
            cursor.execute(name_tokens, [id_tokens[i][1], id_tokens[i][2], id_tokens[i][3], id_tokens[i][4], id_tokens[i][5], id_tokens[i][6], id_tokens[i][7], id_tokens[i][8], id_tokens[i][9]])
            result.append(cursor.fetchone())
        dis = []
        tas = []
        bl = []
        tt = []
        tea = []
        gr = []
        cour = []
        ye = []
        per = []
        for i in range(0, len(result)):
            dis.append(result[i][0])
            tas.append(result[i][1])
            bl.append(result[i][2])
            tt.append(result[i][3])
            tea.append(result[i][4])
            gr.append(result[i][5])
            cour.append(result[i][6])
            ye.append(result[i][7])
            per.append(result[i][8])
        tokens_copy = pd.DataFrame({'Дисциплины': dis,
                                    'Задание': tas,
                                    'Раздел': bl,
                                    'Тип задания': tt,
                                    'Преподаватель': tea,
                                    'Группа': gr,
                                    'Курс': cour,
                                    'Год поступления': ye,
                                    'Сессия': per})
        cursor.execute('SELECT * FROM `schedule`')
        id_schedule = cursor.fetchall()
        result = []
        for i in range(0, len(id_schedule)):
            name_schedule = 'SELECT ' \
                            '(SELECT `name` FROM `subjects` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `teachers` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `groups` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `courses` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `year_enter` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `num_lessons` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `name_day` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `type_week` WHERE `id` = %s) ' \
                            'FROM `schedule`'
            cursor.execute(name_schedule, [id_schedule[i][1], id_schedule[i][2], id_schedule[i][3], id_schedule[i][4], id_schedule[i][5], id_schedule[i][6], id_schedule[i][7], id_schedule[i][8]])
            result.append(cursor.fetchone())
        dis = []
        tea = []
        gr = []
        cour = []
        ye = []
        num_les = []
        nd = []
        tw = []
        for i in range(0, len(result)):
            dis.append(result[i][0])
            tea.append(result[i][1])
            gr.append(result[i][2])
            cour.append(result[i][3])
            ye.append(result[i][4])
            num_les.append(result[i][5])
            nd.append(result[i][6])
            tw.append(result[i][7])
        schedule_copy = pd.DataFrame({'Дисциплина': dis,
                                      'Преподаватель': tea,
                                      'Группа': gr,
                                      'Курс': cour,
                                      'Год поступления': ye,
                                      'Номер пары': num_les,
                                      'День недели': nd,
                                      'Тип недели': tw})
        cursor.execute('SELECT * FROM `schedule_changes`')
        id_schedule_changes = cursor.fetchall()
        for i in range(0, len(id_schedule_changes)):
            name_schedule_changes = 'SELECT ' \
                                    '(SELECT `name` FROM `groups` WHERE `id` = %s), ' \
                                    '(SELECT `name` FROM `courses` WHERE `id` = %s), ' \
                                    '(SELECT `name` FROM `year_enter` WHERE `id` = %s), ' \
                                    '(SELECT `name` FROM `num_lessons` WHERE `id` = %s), ' \
                                    '(SELECT `name` FROM `subjects` WHERE `id` = %s), ' \
                                    '(SELECT `name` FROM `teachers` WHERE `id` = %s), ' \
                                    '(SELECT `date_changes` FROM `schedule_changes` WHERE `id` = %s) ' \
                                    'FROM `schedule_changes`'
            cursor.execute(name_schedule_changes, [id_schedule_changes[i][1], id_schedule_changes[i][2], id_schedule_changes[i][3], id_schedule_changes[i][4], id_schedule_changes[i][5], id_schedule_changes[i][6], id_schedule_changes[i][0]])
            result.append(cursor.fetchone())
        gr = []
        cour = []
        ye = []
        num_les = []
        dis = []
        tea = []
        dc = []
        for i in range(0, len(result)):
            gr.append(result[i][0])
            cour.append(result[i][1])
            ye.append(result[i][2])
            num_les.append(result[i][3])
            dis.append(result[i][4])
            tea.append(result[i][5])
            dc.append(result[i][6])
        schedule_changes_copy = ({'Дисциплина': dis,
                                  'Преподаватель': tea,
                                  'Группа': gr,
                                  'Курс': cour,
                                  'Год поступления': ye,
                                  'Номер пары': num_les,
                                  'Дата замены': dc})
        salary_sheets = {'Вопросы': tokens_copy, 'Расписание': schedule_copy, 'Замены в расписании':schedule_changes_copy}
        writer = pd.ExcelWriter(self.path+'/copy_'+str(datetime.date.today())+'.xlsx', engine='xlsxwriter')

        for sheet_name in salary_sheets.keys():
            salary_sheets[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
        writer.save()

    def open_win_path(self):
        fname = QtWidgets.QFileDialog.getExistingDirectory(None, "Выбрать папку", ".")
        if fname:
            self.filename_2.setText(fname)
            self.path = fname


class Ui_signUp(QtWidgets.QWidget):
    def setupUi(self, Dialog):
        super(Ui_signUp, self).__init__()
        Dialog.setObjectName("Dialog")
        Dialog.resize(570, 375)
        self.uname_lineEdit = QtWidgets.QLineEdit()
        self.password_lineEdit = QtWidgets.QLineEdit()
        self.connect = QtWidgets.QPushButton("connect")
        self.signup_btn = QPushButton(Dialog)
        self.signup_btn.setObjectName("signup_btn")
        self.signup_btn.clicked.connect(Dialog.insertData)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 441, 321))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.combo = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.combo.setObjectName("combo")
        self.combo1 = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.combo1.setObjectName("combo1")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label.setObjectName("label")
        self.label1 = QtWidgets.QLabel(Dialog)
        self.label1.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label1.setObjectName("label1")
        self.label2 = QtWidgets.QLabel(Dialog)
        self.label2.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label2.setObjectName("label2")
        self.label3 = QtWidgets.QLabel(Dialog)
        self.label3.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label3.setObjectName("label3")
        cursor.execute('SELECT `name` FROM `roles`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)):
            self.combo.addItem(check_sel[i][0])
        cursor.execute('SELECT `name` FROM `teachers`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)):
            self.combo1.addItem(check_sel[i][0])
        vl = QVBoxLayout()
        vl.addWidget(self.label)
        vl.addWidget(self.uname_lineEdit)
        vl.addWidget(self.label1)
        vl.addWidget(self.password_lineEdit)
        vl.addWidget(self.label2)
        vl.addWidget(self.combo)
        vl.addWidget(self.label3)
        vl.addWidget(self.combo1)
        vl.addWidget(self.signup_btn)
        self.setLayout(vl)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Регистрация"))
        self.signup_btn.setText(_translate("Dialog", "Зарегистрировать"))
        self.label.setText(_translate("Dialog", "Логин:"))
        self.label1.setText(_translate("Dialog", "Пароль:"))
        self.label2.setText(_translate("Dialog", "Роль:"))
        self.label3.setText(_translate("Dialog", "Преподаватель:"))


class Dialog(QDialog, Ui_signUp):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.setModal(True)
        self.signup_btn.clicked.connect(self.insertData)

    @pyqtSlot()
    def insertData(self):

        username = self.uname_lineEdit.text()
        password = self.password_lineEdit.text()
        role = self.combo.currentText()
        if role == 'Преподаватель':
            teachers = self.combo1.currentText()
        else:
            teachers = None
        if len(password) < 8:
            msg = QMessageBox.information(self, 'Внимание!', 'Пароль должен иметь минимум 8 символов.')
            return
        if (not username) or (not password):
            msg = QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return
        sel_user = 'SELECT * FROM `users` WHERE `login` = %s'
        user = []
        user.append(username)
        cursor.execute(sel_user, user)
        if cursor.fetchone() != None:
            msg = QMessageBox.information(self, 'Внимание!', 'Пользоватеть с таким именем уже зарегистрирован.')
        else:
            sel_role_id = 'SELECT `id` FROM `roles` WHERE `name` = %s'
            role_name = []
            role_name.append(role)
            cursor.execute(sel_role_id, role_name)
            role_id = cursor.fetchone()[0]
            if teachers != None:
                sel_teacher_id = 'SELECT `id` FROM `teachers` WHERE `name` = %s'
                teacher_name = []
                teacher_name.append(teachers)
                cursor.execute(sel_teacher_id, teacher_name)
                teacher_id = cursor.fetchone()[0]
            else:
                teacher_id = None
            in_user = "INSERT INTO `users` (`login`, `password`, `roles_id`, `teachers_id`) VALUES (%s, %s, %s, %s)"
            user.append(password)
            user.append(role_id)
            user.append(teacher_id)
            cursor.execute(in_user, user)
            conn.commit()

    def closeEvent(self, event):
        self.parent.show()


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

    # открыть класс с созданием нового пользователя
    def signUpShow(self):
        self.signUpWindow = Dialog(self)
        self.signUpWindow.show()

    # проверка админ прав
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    # проверка регистрации
    def signUpCheck(self):
        if self.is_admin():
            self.signUpShow()
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)


class Ui_MainWindow(QtWidgets.QWidget):
    # объявление всех кнопок и надписей
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.open_pars_date_week = QtWidgets.QPushButton(self.centralwidget)
        self.open_pars_date_week.setGeometry(QtCore.QRect(250, 130, 89, 25))
        self.open_pars_date_week.setObjectName("open_pars_date_week")
        self.open_pars_date_week.findChild(QPushButton, 'open_pars_date_week')
        self.open_pars_s = QtWidgets.QPushButton(self.centralwidget)
        self.open_pars_s.setGeometry(QtCore.QRect(250, 130, 89, 25))
        self.open_pars_s.setObjectName("open_pars_s")
        self.open_pars_s.findChild(QPushButton, 'open_pars_s')
        self.pars_s = QtWidgets.QPushButton(self.centralwidget)
        self.pars_s.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.pars_s.setObjectName("pars_s")
        self.pars_s.findChild(QPushButton, 'pars_s')
        self.pars_date_week = QtWidgets.QPushButton(self.centralwidget)
        self.pars_date_week.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.pars_date_week.setObjectName("pars_date_week")
        self.pars_date_week.findChild(QPushButton, 'pars_date_week')
        self.auto_copy_btn = QtWidgets.QPushButton(self.centralwidget)
        self.auto_copy_btn.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.auto_copy_btn.setObjectName("auto_copy_btn")
        self.auto_copy_btn.findChild(QPushButton, 'auto_copy_btn')
        self.copy_btn = QtWidgets.QPushButton(self.centralwidget)
        self.copy_btn.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.copy_btn.setObjectName("copy_btn")
        self.copy_btn.findChild(QPushButton, 'copy_btn')
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label.setObjectName("label")
        self.filename = QtWidgets.QLineEdit(self.centralwidget)
        self.filename.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.filename.setObjectName("filename")
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
        self.label_2.setText(_translate("MainWindow", "Укажите путь к папке:"))
        self.label.setText(_translate("MainWindow", "Укажите путь к файлу:"))
        self.open_pars_date_week.setText(_translate("MainWindow", "Обзор..."))
        self.open_pars_s.setText(_translate("MainWindow", "Обзор..."))
        self.pars_date_week.setText(_translate("MainWindow", "Загрузить"))
        self.pars_s.setText(_translate("MainWindow", "Загрузить"))
        self.auto_copy_btn.setText(_translate("MainWindow", "Автоматическое копирование"))
        self.copy_btn.setText(_translate("MainWindow", "Ручное копирование"))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, login):
        sel_test = 'SELECT * FROM `users` WHERE `login` = %s'
        l = []
        l.append(login)
        cursor.execute(sel_test, l)
        self.user = cursor.fetchone()
        super().__init__()
        self.setupUi(self)
        self.parser_date_week_ = QWidget()
        self.reserve_copy_ = QWidget()
        self.parser_s = QWidget()
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.addTab(self.parser_date_week_, "Загрузка даты типов недели")
        self.tabWidget.addTab(self.reserve_copy_, "Резервное копирование")
        self.tabWidget.addTab(self.parser_s, "Загрузка основного расписания")
        self.parser_schedule_Ui()
        self.parser_date_week_Ui()
        self.reserve_copy_Ui()
        self.open_pars_date_week.clicked.connect(self.pars_win_date_week)
        self.pars_date_week.clicked.connect(self.parser_date_week)
        self.open_pars_s.clicked.connect(self.pars_win_schedule)
        self.pars_s.clicked.connect(self.parser_schedule)
        self.copy_btn.clicked.connect(self.reserve_copy)

    def reserve_copy_Ui(self):
        vl = QVBoxLayout(self)
        self.tabWidget = QTabWidget(self.centralwidget)
        vl.addWidget(self.auto_copy_btn)
        vl.addWidget(self.copy_btn)
        self.tabWidget.setTabText(1, "ReserveCopy")
        self.reserve_copy_.setLayout(vl)

    def reserve_copy(self):
        self.Copy = ReserveCopy()
        self.Copy.show()

    def parser_date_week_Ui(self):
        hlayout = QHBoxLayout(self)
        self.tabWidget = QTabWidget(self.centralwidget)
        hlayout.addWidget(self.label_2)
        hlayout.addWidget(self.filename_2)
        hlayout.addWidget(self.open_pars_date_week)
        vlayout = QVBoxLayout(self)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.pars_date_week)
        self.tabWidget.setTabText(0, "Parser")
        self.parser_date_week_.setLayout(vlayout)

    def parser_date_week(self):
        df = pd.read_excel(io=self.file_, engine='openpyxl', sheet_name='Лист1')
        arr = list(df.head(0))

        # Парс excel
        result = []

        # Парс ДАТ НЕДЕЛЬ
        for n in range(0, len(arr)):
            for i in range(0, len(df[arr[n]].tolist())):
                dates = df[arr[n]].tolist()[i]
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
                res = pd.date_range(min(start_date, end_date), max(start_date, end_date)).strftime('%Y-%m-%d').tolist()
                for j in range(0, len(res)):
                    cursor.execute("SELECT `id` FROM `type_week` WHERE `name` LIKE %s", [arr[n]])
                    result.append(cursor.fetchone()[0])
                    result.append(res[j])
                    add_res = 'INSERT INTO `date_type_week` (`type_week_id`, `date_week`) VALUES (%s, %s)'
                    cursor.execute(add_res, result)
                    conn.commit()
                    result = []

    def pars_win_date_week(self):
        self.open_pars_date_week.hide()
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './', '(*.xls *.xlsx)')
        if fname:
            self.filename_2.setText(fname)
            self.file_ = str(fname)

    def parser_schedule(self):

        df = pd.read_excel(io=self.file_s, engine='openpyxl', sheet_name='Лист1')
        excel = openpyxl.load_workbook(filename=self.file_s)
        sheet = excel.worksheets[0]

        # Парс excel
        result = []

        for r in sheet.merged_cells.ranges:
            cl, rl, cr, rr = r.bounds  # границы объединенной области
            rl -= 2
            rr -= 1
            cl -= 1
            base_value = df.iloc[rl, cl]
            df.iloc[rl:rr, cl:cr] = base_value

        # Парс ДНЕЙ
        for i in range(0, len(df['Дни'].tolist())):
            add_ser = 'INSERT INTO `name_day` (`name`) VALUES (%s)'
            result.append(df['Дни'].tolist()[i])
            check_input = 'SELECT * FROM `name_day` WHERE `name` = %s'
            cursor.execute(check_input, result)
            if cursor.fetchone() == None:
                cursor.execute(add_ser, result)
                conn.commit()
                result = []
            else:
                result = []

        # Парс ПАР
        for i in range(0, len(df['Уроки'].tolist())):
            add_ser = 'INSERT INTO `num_lessons` (`name`) VALUES (%s)'
            result.append(df['Уроки'].tolist()[i])
            check_input = 'SELECT * FROM `num_lessons` WHERE `name` = %s'
            cursor.execute(check_input, result)
            if cursor.fetchone() == None:
                cursor.execute(add_ser, result)
                conn.commit()
                result = []
            else:
                result = []

        # Парс ТИПА НЕДЕЛИ
        for i in range(0, len(df['Unnamed: 2'].tolist())):
            add_ser = 'INSERT INTO `type_week` (`name`) VALUES (%s)'
            result.append(df['Уроки'].tolist()[i])
            check_input = 'SELECT * FROM `type_week` WHERE `name` = %s'
            cursor.execute(check_input, result)
            if cursor.fetchone() == None:
                cursor.execute(add_ser, result)
                conn.commit()
                result = []
            else:
                result = []

        # Парс

    def parser_schedule_Ui(self):
        hlayout = QHBoxLayout(self)
        self.tabWidget = QTabWidget(self.centralwidget)
        hlayout.addWidget(self.label)
        hlayout.addWidget(self.filename)
        hlayout.addWidget(self.open_pars_s)
        vlayout = QVBoxLayout(self)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.pars_s)
        self.tabWidget.setTabText(2, "ParserS")
        self.parser_s.setLayout(vlayout)

    def pars_win_schedule(self):
        self.open_pars_s.hide()
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './', '(*.xls *.xlsx)')
        if fname:
            self.filename.setText(fname)
            self.file_s = str(fname)


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

#+++++++++++++++++++++++++++++++++++++++++++++++++++
'''
Доделать создание резервной копии !!!!!!<---
Сделать парсер расписания
Сделать парсер замен в раснисание
Сделать парсер часов занятий
Сделать автоматический подстчёт часов
Сделать график с текущеми показателями выполнения работы
Сделать помошника для подсчёта часов
Сдеалть вывод отчёта по вычитаным часам
Сделать отправку отчёта по заданной дате
'''
