import mysql.connector
import ctypes, sys
import os, os.path
import json
import shutil
import random
import pandas as pd
import aspose.words as aw
from aspose.cells import Workbook, SaveFormat, FileFormatType
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, \
    QPushButton, QMainWindow, QLabel
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QStyleFactory, QLabel, QPushButton, QPlainTextEdit, QApplication, QCheckBox, QMainWindow,
                             QWidget,
                             QVBoxLayout, QTabWidget)
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import *
from PyQt5.Qt import *


class Ui_UploadUsers(QtWidgets.QWidget):
    def setupUi(self, UploadUsers):
        UploadUsers.setObjectName("UploadUsers")
        UploadUsers.resize(496, 265)
        self.open_pars = QtWidgets.QPushButton(UploadUsers)
        self.open_pars.setGeometry(QtCore.QRect(250, 130, 89, 25))
        self.open_pars.setObjectName("open_pars")
        self.open_pars.findChild(QPushButton, 'open_pars')
        self.filename_2 = QtWidgets.QLineEdit(UploadUsers)
        self.filename_2.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.filename_2.setObjectName("filename_2")
        self.pars_ = QtWidgets.QPushButton(UploadUsers)
        self.pars_.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.pars_.setObjectName("pars_")
        self.pars_.findChild(QPushButton, 'pars_')
        self.label_2 = QtWidgets.QLabel(UploadUsers)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_2.setObjectName("label_2")
        self.retranslateUi(UploadUsers)
        QtCore.QMetaObject.connectSlotsByName(UploadUsers)

    def retranslateUi(self, UploadUsers):
        _translate = QCoreApplication.translate
        UploadUsers.setWindowTitle(_translate("UploadUsers", "Создание учётной записи для пользователей"))
        self.label_2.setText(_translate("UploadUsers", "Укажите путь к файлу:"))
        self.open_pars.setText(_translate("UploadUsers", "Обзор..."))
        self.pars_.setText(_translate("UploadUsers", "Загрузить"))


class UploadUsers(QtWidgets.QDialog, Ui_UploadUsers):

    def __init__(self, parent=None):
        super(UploadUsers, self).__init__(parent)
        self.setupUi(self)
        hl = QHBoxLayout()
        hl.addWidget(self.label_2)
        hl.addWidget(self.filename_2)
        hl.addWidget(self.open_pars)
        vl = QVBoxLayout()
        vl.addLayout(hl)
        vl.addWidget(self.pars_)
        self.setLayout(vl)
        self.pars_.clicked.connect(self.parser)
        self.open_pars.clicked.connect(self.pars_win)

    def parser(self):
        dic = {'Ь': '', 'ь': '', 'Ъ': '', 'ъ': '', 'А': 'A', 'а': 'a', 'Б': 'B', 'б': 'b', 'В': 'V', 'в': 'v',
               'Г': 'G', 'г': 'g', 'Д': 'D', 'д': 'd', 'Е': 'E', 'е': 'e', 'Ё': 'E', 'ё': 'e', 'Ж': 'Zh', 'ж': 'zh',
               'З': 'Z', 'з': 'z', 'И': 'I', 'и': 'i', 'Й': 'I', 'й': 'i', 'К': 'K', 'к': 'k', 'Л': 'L', 'л': 'l',
               'М': 'M', 'м': 'm', 'Н': 'N', 'н': 'n', 'О': 'O', 'о': 'o', 'П': 'P', 'п': 'p', 'Р': 'R', 'р': 'r',
               'С': 'S', 'с': 's', 'Т': 'T', 'т': 't', 'У': 'U', 'у': 'u', 'Ф': 'F', 'ф': 'f', 'Х': 'Kh', 'х': 'kh',
               'Ц': 'Tc', 'ц': 'tc', 'Ч': 'Ch', 'ч': 'ch', 'Ш': 'Sh', 'ш': 'sh', 'Щ': 'Shch', 'щ': 'shch', 'Ы': 'Y',
               'ы': 'y', 'Э': 'E', 'э': 'e', 'Ю': 'Iu', 'ю': 'iu', 'Я': 'Ia', 'я': 'ia'}

        alphabet = ['Ь', 'ь', 'Ъ', 'ъ', 'А', 'а', 'Б', 'б', 'В', 'в', 'Г', 'г', 'Д', 'д', 'Е', 'е', 'Ё', 'ё',
                    'Ж', 'ж', 'З', 'з', 'И', 'и', 'Й', 'й', 'К', 'к', 'Л', 'л', 'М', 'м', 'Н', 'н', 'О', 'о',
                    'П', 'п', 'Р', 'р', 'С', 'с', 'Т', 'т', 'У', 'у', 'Ф', 'ф', 'Х', 'х', 'Ц', 'ц', 'Ч', 'ч',
                    'Ш', 'ш', 'Щ', 'щ', 'Ы', 'ы', 'Э', 'э', 'Ю', 'ю', 'Я', 'я']

        arr_word = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j',
                    'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '']
        arr_word_up = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J',
                       'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '']
        arr_num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '']

        with open('config_db.json', encoding="utf8") as save:
            json_db = json.load(save)

        self.list = []

        # Подключение к БД
        conn = mysql.connector.connect(user=json_db[0]['login'], password=json_db[0]['password'],
                                       host=json_db[0]['host'],
                                       database=json_db[0]['name_db'])
        cursor = conn.cursor(buffered=True)
        df = pd.read_excel(io=self.file_, engine='openpyxl', sheet_name='Лист1')

        # Парс excel
        result = []

        # Парс пользователей
        for i in range(0, len(df['Пользователь'].tolist())):
            role = []
            role.append(df['Роль'].tolist()[i])
            check_input = 'SELECT * FROM `roles` WHERE `name` = %s'
            cursor.execute(check_input, role)
            data_role = cursor.fetchone()
            if data_role != None:
                if role[0] == 'Преподаватель':
                    role.append(df['Пользователь'].tolist()[i])
                    tea_name = []
                    tea_name.append(role[1])
                    sel_id_tea = 'SELECT `id` FROM `teachers` WHERE `name` = %s'
                    cursor.execute(sel_id_tea, tea_name)
                    res_id_tea = cursor.fetchone()
                    if res_id_tea == None:
                        in_tea = 'INSERT INTO `teachers` (`name`) VALUES (%s)'
                        cursor.execute(in_tea, tea_name)
                        conn.commit()
                        sel_id_tea = 'SELECT `id` FROM `teachers` WHERE `name` = %s'
                        cursor.execute(sel_id_tea, tea_name)
                        id_tea = cursor.fetchone()[0]
                    else:
                        id_tea = res_id_tea[0]
                else:
                    role.append(df['Пользователь'].tolist()[i])
                    id_tea = None
                login = ''
                len_st = len(role[1])
                for j in range(0, len_st):
                    if role[1][j] in alphabet:
                        simb = dic[role[1][j]]
                    else:
                        simb = role[1][j]
                    login += simb
                num = 8
                password = ''
                for j in range(0, num):
                    arr_ran = random.randint(0, 2)
                    if arr_ran == 0:
                        sim = random.randint(0, len(arr_word) - 1)
                        password += arr_word[sim]
                    elif arr_ran == 1:
                        sim = random.randint(0, len(arr_word_up) - 1)
                        password += arr_word_up[sim]
                    elif arr_ran == 2:
                        sim = random.randint(0, len(arr_num) - 1)
                        password += arr_num[sim]
                result.append(login)
                result.append(password)
                result.append(data_role[0])
                result.append(id_tea)
                in_user = "INSERT INTO `users` (`login`, `password`, `roles_id`, `teachers_id`) VALUES (%s, %s, %s, %s)"
                cursor.execute(in_user, result)
                conn.commit()
                result = []
                name_login = []
                name_login.append(login)
                name_login.append(role[1])
                self.list.append(name_login)
            else:
                self.dlg = QMessageBox()
                self.dlg.addButton("Ок", QMessageBox.AcceptRole)
                self.dlg.setIcon(QMessageBox.Warning)
                self.dlg.setWindowTitle("Ошибка")
                self.dlg.setInformativeText(
                    "Ошибка в названии роли " + str(df['Роль'].tolist()[i]) + "!")
                bttn = self.dlg.exec()
        self.dlg = QMessageBox()
        self.dlg.addButton("Да", QMessageBox.AcceptRole)
        self.dlg.addButton("Нет", QMessageBox.AcceptRole)
        self.dlg.setIcon(QMessageBox.Information)
        self.dlg.setWindowTitle("Оповещение")
        self.dlg.setInformativeText(
            "Пользователи успешно созданы! Вывести данные авторизации для каждого пользоавтеля?")
        bttn = self.dlg.exec()
        if self.dlg.clickedButton().text() == "Да":
            self.output_user()

    def output_user(self):
        doc = aw.Document()
        builder = aw.DocumentBuilder(doc)
        table = builder.start_table()
        builder.insert_cell()
        table.left_indent = 20.0
        builder.row_format.height = 40.0
        builder.row_format.height_rule = aw.HeightRule.AT_LEAST
        builder.paragraph_format.alignment = aw.ParagraphAlignment.CENTER
        builder.font.size = 16
        builder.font.name = "Times New Romans"
        builder.font.bold = True
        builder.cell_format.width = 100.0
        builder.write("ФИО\n сотрудника")
        builder.insert_cell()
        builder.write("Логин")
        builder.insert_cell()
        builder.cell_format.width = 100.0
        builder.write("Пароль")
        builder.end_row()
        builder.cell_format.width = 100.0
        builder.cell_format.vertical_alignment = aw.tables.CellVerticalAlignment.CENTER
        builder.row_format.height = 30.0
        builder.row_format.height_rule = aw.HeightRule.AUTO
        builder.insert_cell()
        builder.font.size = 12
        builder.font.bold = False
        with open('config_db.json', encoding="utf8") as save:
            json_db = json.load(save)

        # Подключение к БД
        conn = mysql.connector.connect(user=json_db[0]['login'], password=json_db[0]['password'],
                                       host=json_db[0]['host'],
                                       database=json_db[0]['name_db'])
        cursor = conn.cursor(buffered=True)
        result = []
        for n in range(0, len(self.list)):
            data = []
            login = []
            login.append(self.list[n][0])
            sel_uchet = 'SELECT `login`, `password` FROM `users` WHERE `login` = %s'
            cursor.execute(sel_uchet, login)
            data_uch = cursor.fetchone()
            for i in range(0, len(data_uch)):
                data.append(data_uch[i])
            data.append(self.list[n][1])
            result.append(data)
        for g in range(0, len(result)):
            builder.cell_format.width = 100.0
            builder.write(str(result[g][2]))
            builder.insert_cell()
            builder.write(str(result[g][0]))
            builder.insert_cell()
            builder.write(str(result[g][1]))
            builder.end_row()
            if g < len(result) - 1:
                builder.insert_cell()
        builder.end_table()
        doc.save('Логины и пароли.docx')

    def pars_win(self):
        self.open_pars.hide()
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './', '(*.xls *.xlsx)')
        self.file_ = ''
        if fname:
            self.filename_2.setText(fname)
            self.file_ += str(fname)


class Ui_CreateAdmin(QtWidgets.QWidget):
    def setupUi(self, CreateAdmin):
        CreateAdmin.setObjectName("CreateAdmin")
        CreateAdmin.resize(496, 265)
        self.login_line = QtWidgets.QLineEdit(CreateAdmin)
        self.login_line.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.login_line.setObjectName("login_line")
        self.password_line = QtWidgets.QLineEdit(CreateAdmin)
        self.password_line.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.password_line.setObjectName("password_line")
        self.save_btn = QtWidgets.QPushButton(CreateAdmin)
        self.save_btn.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.save_btn.setObjectName("save_btn")
        self.retranslateUi(CreateAdmin)
        QtCore.QMetaObject.connectSlotsByName(CreateAdmin)

    def retranslateUi(self, CreateAdmin):
        _translate = QCoreApplication.translate
        CreateAdmin.setWindowTitle(_translate("CreateAdmin", "Создание учётной записи для админа"))
        self.login_line.setText(_translate("CreateAdmin", "Логин:"))
        self.password_line.setText(_translate("CreateAdmin", "Пароль:"))
        self.save_btn.setText(_translate("CreateAdmin", "Сохранить:"))


class CreateAdmin(QtWidgets.QDialog, Ui_CreateAdmin):
    def __init__(self, parent=None):
        super(CreateAdmin, self).__init__(parent)
        self.setupUi(self)
        vl = QVBoxLayout(self)
        vl.addWidget(self.login_line)
        vl.addWidget(self.password_line)
        vl.addWidget(self.save_btn)
        self.setLayout(vl)
        self.save_btn.clicked.connect(self.create_admin)

    def create_admin(self):
        data = []
        with open('config_db.json', encoding="utf8") as save:
            json_db = json.load(save)

        # Подключение к БД
        conn = mysql.connector.connect(user=json_db[0]['login'], password=json_db[0]['password'],
                                       host=json_db[0]['host'],
                                       database=json_db[0]['name_db'])
        cursor = conn.cursor(buffered=True)
        data.append(self.login_line.text())
        data.append(self.password_line.text())
        cursor.execute("SELECT `id` FROM `roles` WHERE `name` = 'Администратор'")
        data.append(cursor.fetchone()[0])
        data.append(None)
        check_admin = 'SELECT EXISTS(SELECT * FROM `users` WHERE `login` = %s AND `password` = %s AND `roles_id` = %s AND ' \
                      '`teachers_id` = %s)'
        cursor.execute(check_admin, data)
        if cursor.fetchone()[0] == False:
            in_user_admin = 'INSERT INTO `users` (`login`, `password`, `roles_id`, `teachers_id`) VALUES (%s, %s, %s, %s)'
            cursor.execute(in_user_admin, data)
            conn.commit()
            self.dlg = QMessageBox()
            self.dlg.addButton("Ок", QMessageBox.AcceptRole)
            self.dlg.setIcon(QMessageBox.Information)
            self.dlg.setWindowTitle("Оповещение")
            self.dlg.setInformativeText(
                "Учётная запись была создана успешна!")
            bttn = self.dlg.exec()
            if self.dlg.clickedButton().text() == "Вручную":
                self.CA = CreateAdmin(self)
                self.CA.show()
        else:
            self.dlg = QMessageBox()
            self.dlg.addButton("Ок", QMessageBox.AcceptRole)
            self.dlg.setIcon(QMessageBox.Information)
            self.dlg.setWindowTitle("Оповещение")
            self.dlg.setInformativeText(
                "Учётная запись с такими данными уже существует. Используйте ее входа или создайте новую.")
            bttn = self.dlg.exec()


class Ui_OptionsDB(QtWidgets.QWidget):
    def setupUi(self, OptionsDB):
        OptionsDB.setObjectName("OptionsDB")
        OptionsDB.resize(496, 265)
        self.label_2 = QtWidgets.QLabel(OptionsDB)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(OptionsDB)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(OptionsDB)
        self.label_4.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(OptionsDB)
        self.label_5.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_5.setObjectName("label_5")
        self.name_line = QtWidgets.QLineEdit(OptionsDB)
        self.name_line.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.name_line.setObjectName("name_line")
        self.pass_line = QtWidgets.QLineEdit(OptionsDB)
        self.pass_line.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.pass_line.setObjectName("pass_line")
        self.host_line = QtWidgets.QLineEdit(OptionsDB)
        self.host_line.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.host_line.setObjectName("host_line")
        self.db_line = QtWidgets.QLineEdit(OptionsDB)
        self.db_line.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.db_line.setObjectName("db_line")
        self.save_btn = QtWidgets.QPushButton(OptionsDB)
        self.save_btn.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.save_btn.setObjectName("save_btn")
        self.retranslateUi(OptionsDB)
        QtCore.QMetaObject.connectSlotsByName(OptionsDB)

    def retranslateUi(self, OptionsDB):
        _translate = QCoreApplication.translate
        OptionsDB.setWindowTitle(_translate("OptionsDB", "Конфигурация базы данных"))
        self.label_2.setText(_translate("OptionsDB", "Логин:"))
        self.label_3.setText(_translate("OptionsDB", "Пароль:"))
        self.label_4.setText(_translate("OptionsDB", "Хост:"))
        self.label_5.setText(_translate("OptionsDB", "База данных:"))
        self.save_btn.setText(_translate("OptionsDB", "Сохранить"))


class OptionsDB(QtWidgets.QDialog, Ui_OptionsDB):
    def __init__(self, parent=None):
        super(OptionsDB, self).__init__(parent)
        self.setupUi(self)
        vl = QVBoxLayout(self)
        vl.addWidget(self.label_2)
        vl.addWidget(self.name_line)
        vl.addWidget(self.label_3)
        vl.addWidget(self.pass_line)
        vl.addWidget(self.label_4)
        vl.addWidget(self.host_line)
        vl.addWidget(self.label_5)
        vl.addWidget(self.db_line)
        vl.addWidget(self.save_btn)
        self.setLayout(vl)
        self.save_btn.clicked.connect(self.save_)

    def check_save(self):
        return os.path.exists('config_db.json')

    def save_(self):
        if self.check_save():
            data = [{'login': self.name_line.text(), 'password': self.pass_line.text(), 'host': self.host_line.text(),
                     'name_db': self.db_line.text()}]
            with open('config_db.json', 'w') as save:
                json.dump(data, save)
        else:
            workbook = Workbook()
            worksheet = workbook.worksheets[0]

            worksheet.cells.get("A1").put_value("login")
            worksheet.cells.get("B1").put_value("password")
            worksheet.cells.get("C1").put_value("host")
            worksheet.cells.get("D1").put_value("name_db")
            worksheet.cells.get("A2").put_value(self.name_line.text())
            worksheet.cells.get("B2").put_value(self.pass_line.text())
            worksheet.cells.get("C2").put_value(self.host_line.text())
            worksheet.cells.get("D2").put_value(self.db_line.text())

            workbook.save("config_db.json")


class Ui_OptionsFiles(QtWidgets.QWidget):
    def setupUi(self, OptionsFiles):
        OptionsFiles.setObjectName("OptionsFiles")
        OptionsFiles.resize(496, 265)
        self.save_path_conf_db = QtWidgets.QPushButton(OptionsFiles)
        self.save_path_conf_db.setGeometry(QtCore.QRect(250, 130, 89, 25))
        self.save_path_conf_db.setObjectName("save_path_conf_db")
        self.save_path_conf_db.findChild(QPushButton, 'save_path_conf_db')
        self.open_win_path_conf_db = QtWidgets.QPushButton(OptionsFiles)
        self.open_win_path_conf_db.setGeometry(QtCore.QRect(250, 130, 89, 25))
        self.open_win_path_conf_db.setObjectName("open_win_path_conf_db")
        self.open_win_path_conf_db.findChild(QPushButton, 'open_win_path_conf_db')
        self.filename_2 = QtWidgets.QLineEdit(OptionsFiles)
        self.filename_2.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.filename_2.setObjectName("filename_2")
        self.label_2 = QtWidgets.QLabel(OptionsFiles)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_2.setObjectName("label_2")
        self.retranslateUi(OptionsFiles)
        QtCore.QMetaObject.connectSlotsByName(OptionsFiles)

    def retranslateUi(self, OptionsFiles):
        _translate = QCoreApplication.translate
        OptionsFiles.setWindowTitle(_translate("OptionsFiles", "Конфигурация базы данных"))
        self.open_win_path_conf_db.setText(_translate("OptionsFiles", "Обзор..."))
        self.save_path_conf_db.setText(_translate("OptionsFiles", "Сохранить"))
        self.label_2.setText(
            _translate("OptionsFiles", "Укажите путь куда будет перемещён файл конфигураций базы данных"))


class OptionsFiles(QtWidgets.QDialog, Ui_OptionsFiles):
    def __init__(self, parent=None):
        super(OptionsFiles, self).__init__(parent)
        self.setupUi(self)
        hl = QHBoxLayout()
        hl.addWidget(self.label_2)
        hl.addWidget(self.filename_2)
        hl.addWidget(self.open_win_path_conf_db)
        vl = QVBoxLayout()
        vl.addLayout(hl)
        vl.addWidget(self.save_path_conf_db)
        self.setLayout(vl)
        self.open_win_path_conf_db.clicked.connect(self.open_win_path)
        self.save_path_conf_db.clicked.connect(self.move_file_to_folder)

    def open_win_path(self):
        fname = QtWidgets.QFileDialog.getExistingDirectory(None, "Выбрать папку", ".")
        if fname:
            self.filename_2.setText(fname)
            self.path = fname

    def move_file_to_folder(self):
        shutil.move('config_db.json', self.path)
        if self.check_save():
            data = [{'config_db': self.path}]
            with open('config_path.json', 'w') as save:
                json.dump(data, save)
        else:
            workbook = Workbook()
            worksheet = workbook.worksheets[0]

            worksheet.cells.get("A1").put_value("config_db")
            worksheet.cells.get("A2").put_value(self.path)

            workbook.save("config_path.json")

    def check_save(self):
        return os.path.exists('config_path.json')


class Ui_MainWindow(QtWidgets.QWidget):

    # объявление всех кнопок и надписей
    def setupUi(self, MainWindow):
        super(Ui_MainWindow, self).__init__()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(496, 265)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.options_db = QtWidgets.QPushButton(self.centralwidget)
        self.options_db.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.options_db.setObjectName("options_db")
        self.upload_db = QtWidgets.QPushButton(self.centralwidget)
        self.upload_db.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.upload_db.setObjectName("upload_db")

        self.upload_users_btn = QtWidgets.QPushButton(self.centralwidget)
        self.upload_users_btn.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.upload_users_btn.setObjectName("upload_users_btn")
        self.options_files_btn = QtWidgets.QPushButton(self.centralwidget)
        self.options_files_btn.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.options_files_btn.setObjectName("options_files_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # подпись надписей и кнопок
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Кофигуратор"))
        self.options_db.setText(_translate("MainWindow", "Настроить базу данных"))
        self.upload_db.setText(_translate("MainWindow", "Заполнить базу данных"))
        self.upload_users_btn.setText(_translate("MainWindow", "Загрузить список пользователей"))
        self.options_files_btn.setText(_translate("MainWindow", "Конфигурация файлов"))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        vl = QVBoxLayout(self.centralwidget)
        vl.addWidget(self.options_db)
        vl.addWidget(self.upload_db)
        vl.addWidget(self.upload_users_btn)
        vl.addWidget(self.options_files_btn)
        self.setLayout(vl)
        self.options_db.clicked.connect(self.optionsDB)
        self.upload_db.clicked.connect(self.uploadDB)
        self.upload_users_btn.clicked.connect(self.upload_users)
        self.options_files_btn.clicked.connect(self.options_files)

    def options_files(self):
        self.OF = OptionsFiles(self)
        self.OF.show()

    def upload_users(self):
        self.UU = UploadUsers(self)
        self.UU.show()

    def connectDB(self):
        with open('config_db.json', encoding="utf8") as save:
            json_db = json.load(save)
        # Подключение к БД
        conn = mysql.connector.connect(user=json_db[0]['login'], password=json_db[0]['password'],
                                       host=json_db[0]['host'],
                                       database=json_db[0]['name_db'])
        return conn

    def uploadDB(self):
        conn = self.connectDB()
        cursor = conn.cursor(buffered=True)
        cursor.execute('create table `organization` (id int primary key auto_increment, `name` text)')
        conn.commit()
        cursor.execute('create table if not exists `subjects` (id int primary key auto_increment, `name` text)')
        conn.commit()
        cursor.execute('create table if not exists `year_enter` (id int primary key auto_increment, `name` text)')
        conn.commit()
        cursor.execute('create table if not exists `teachers` (id int primary key auto_increment, `name` text)')
        conn.commit()
        cursor.execute('create table if not exists `tasks` (id int primary key auto_increment, `name` text)')
        conn.commit()
        cursor.execute('create table if not exists `type_tasks` (id int primary key auto_increment, `name` text)')
        conn.commit()
        cursor.execute('create table if not exists `blocks` (id int primary key auto_increment, `name` text)')
        conn.commit()
        cursor.execute('create table if not exists `periods` (id int primary key auto_increment, `name` text)')
        conn.commit()
        cursor.execute('create table if not exists `groups` (id int primary key auto_increment, `name` text)')
        conn.commit()
        cursor.execute('create table if not exists `courses` (id int primary key auto_increment, `name` text)')
        conn.commit()
        cursor.execute('create table if not exists `roles` (id int primary key auto_increment, `name` text)')
        conn.commit()
        cursor.execute('create table if not exists `tokens` (id int primary key auto_increment, `subjects_id` int, '
                       '`tasks_id` int, `type_tasks_id` int, `teachers_id` int, `groups_id` int, `courses_id` int, '
                       '`year_enter_id` int, `periods_id` int, `blocks_id` int, `organization_id` int, foreign key ('
                       'subjects_id) references subjects (id), foreign key (tasks_id) references tasks (id), '
                       'foreign key (type_tasks_id) references type_tasks (id), foreign key (teachers_id) references '
                       'teachers (id), foreign key (groups_id) references `groups` (id), foreign key (courses_id) '
                       'references courses (id), foreign key (year_enter_id) references year_enter (id), foreign key '
                       '(periods_id) references periods (id), foreign key (blocks_id) references blocks (id), '
                       'foreign key (organization_id) references organization (id))')
        conn.commit()
        cursor.execute('create table if not exists `exam_tokens` (id int primary key auto_increment, `number` text, '
                       '`tokens_id` int, `date_exam` date, `set` varchar(3), foreign key (tokens_id) references '
                       'tokens (id))')
        conn.commit()
        cursor.execute(
            'create table if not exists `users` (id int primary key auto_increment, login text, `password` text, '
            'roles_id int, teachers_id int, foreign key (roles_id) references `roles` (id), foreign key (teachers_id) '
            'references teachers (id))')
        conn.commit()
        self.input_org()
        roles_arr = ['Преподаватель', 'Учебная часть', 'Администратор']
        for i in range(0, len(roles_arr)):
            role_name = []
            role_name.append(roles_arr[i])
            sel_role_name = 'SELECT EXISTS(SELECT id FROM `roles` WHERE `name` = %s)'
            cursor.execute(sel_role_name, role_name)
            if cursor.fetchone()[0] == False:
                in_role = 'INSERT INTO `roles` (`name`) VALUES (%s)'
                cursor.execute(in_role, role_name)
                conn.commit()
        cursor.execute("SELECT `id` FROM `roles` WHERE `name` = 'Администратор'")
        id_role_admin = cursor.fetchone()
        sel_admin = 'SELECT EXISTS(SELECT * FROM `users` WHERE `roles_id` = %s)'
        cursor.execute(sel_admin, id_role_admin)
        if cursor.fetchone()[0] == False:
            self.dlg = QMessageBox()
            self.dlg.addButton("Автоматически", QMessageBox.AcceptRole)
            self.dlg.addButton("Вручную", QMessageBox.AcceptRole)
            self.dlg.setIcon(QMessageBox.Information)
            self.dlg.setWindowTitle("Оповещение")
            self.dlg.setInformativeText(
                "Как создать аккаунт администратора автоматически или вручную?")
            bttn = self.dlg.exec()
            if self.dlg.clickedButton().text() == "Вручную":
                self.CA = CreateAdmin(self)
                self.CA.show()
            elif self.dlg.clickedButton().text() == "Автоматически":
                cursor.execute(
                    "INSERT INTO `users` (`login`, `password`, `roles_id`, `teachers_id`) VALUES ('admin', 'admin1', %s, NULL)",
                    id_role_admin)
                conn.commit()
                self.dlg = QMessageBox()
                self.dlg.addButton("Ок", QMessageBox.AcceptRole)
                self.dlg.setIcon(QMessageBox.Information)
                self.dlg.setWindowTitle("Оповещение")
                self.dlg.setInformativeText(
                    "Учётная запись администратора создана успешно! Данные для входа: логин: admin | пароль: admin1")
                bttn = self.dlg.exec()

    def input_org(self):
        self.org_line = QtWidgets.QLineEdit()
        self.org_line.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.org_line.setObjectName("org_line")
        conn = self.connectDB()
        cursor = conn.cursor(buffered=True)
        text, ok = QInputDialog.getText(self, 'Название организации', 'Название организации')
        if ok:
            self.org_line.setText(str(text))
        in_org = 'INSERT INTO `organization` (`name`) VALUES (%s)'
        org_name = []
        org_name.append(self.org_line.text())
        cursor.execute(in_org, org_name)
        conn.commit()

    def optionsDB(self):
        self.ODB = OptionsDB(self)
        self.ODB.show()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        app.setStyle('Fusion')
        splash = QtWidgets.QSplashScreen()
        splash.setPixmap(QtGui.QPixmap('images/splash1.jpg'))
        splash.show()
        splash.showMessage('<h1 style="color:#000c36;">Добро пожаловать в Кофигуратор Деканат (beta)</h1>',
                           QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft, QtCore.Qt.white)
        QtCore.QThread.msleep(5000)
        w = MainWindow()
        w.show()
        splash.hide()
        sys.exit(app.exec_())
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
