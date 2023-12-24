import pandas as pd
import mysql.connector
import random
import aspose.words as aw
import ctypes, sys
import os
import math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, \
    QPushButton, QMainWindow, QLabel
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QLabel, QPushButton, QPlainTextEdit, QApplication, QCheckBox, QMainWindow, QWidget,
                             QVBoxLayout, QTabWidget)
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

# Подключение к БД
conn = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='tokens')
cursor = conn.cursor(buffered=True)


class Ui_MainWindow(QtWidgets.QWidget):

    # объявление всех кнопок и надписей
    def setupUi(self, MainWindow):
        super(Ui_MainWindow, self).__init__()
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        layoutV = QVBoxLayout(self)
        layoutV.addWidget(self.scroll)
        self.widget = QWidget()
        self.scroll.setWidget(self.widget)
        self.open_pars = QtWidgets.QPushButton(self.centralwidget)
        self.open_pars.setGeometry(QtCore.QRect(250, 130, 89, 25))
        self.open_pars.setObjectName("open_pars")
        self.open_pars.findChild(QPushButton, 'open_pars')
        self.output_token = QtWidgets.QTextEdit(self.centralwidget)
        self.output_token.setMinimumSize(QtCore.QSize(0, 50))
        self.output_token.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.output_token.setObjectName("output_token")
        self.pars_ = QtWidgets.QPushButton(self.centralwidget)
        self.pars_.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.pars_.setObjectName("pars_")
        self.pars_.findChild(QPushButton, 'pars_')
        self.output_ = QtWidgets.QPushButton(self.centralwidget)
        self.output_.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.output_.setObjectName("output_")
        self.output_.findChild(QPushButton, 'output_')
        self.next_ = QtWidgets.QPushButton(self.centralwidget)
        self.next_.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.next_.setObjectName("next_")
        self.next_.findChild(QPushButton, 'next_')
        self.gen_b = QtWidgets.QPushButton(self.centralwidget)
        self.gen_b.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.gen_b.setObjectName("gen_b")
        self.gen_b.findChild(QPushButton, 'gen_b')
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_1.setObjectName("label_1")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_11.setObjectName("label_11")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_17.setObjectName("label_17")
        self.tokens_line = QtWidgets.QLineEdit(self.centralwidget)
        self.tokens_line.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.tokens_line.setObjectName("tokens_line")
        self.tasks_line = QtWidgets.QLineEdit(self.centralwidget)
        self.tasks_line.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.tasks_line.setObjectName("tasks_line")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_2.setObjectName("label_2")
        self.filename_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.filename_2.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.filename_2.setObjectName("filename_2")
        self.checkBox_practic_out = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_practic_out.setGeometry(QtCore.QRect(170, 120, 81, 20))
        self.checkBox_practic_out.setObjectName('checkBox_practic_out')
        self.checkBox_practic_gen = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_practic_gen.setGeometry(QtCore.QRect(170, 120, 81, 20))
        self.checkBox_practic_gen.setObjectName('checkBox_practic_gen')
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

    # подпись надписей и кнопок
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Генератор билетов"))
        # Надписи (label)
        self.label_10.setText(_translate("MainWindow", "Введите кол-во заданий из одного раздела:"))
        self.label_17.setText(_translate("MainWindow", "Выберите период:"))
        self.label_16.setText(_translate("MainWindow", "Выберите год поступления:"))
        self.label_15.setText(_translate("MainWindow", "Выберите курс:"))
        self.label_14.setText(_translate("MainWindow", "Выберите группу:"))
        self.label_13.setText(_translate("MainWindow", "Выберите преподавателя:"))
        self.label_11.setText(_translate("MainWindow", "Выберите дисциплину:"))
        self.label_7.setText(_translate("MainWindow", "Выберите период:"))
        self.label_6.setText(_translate("MainWindow", "Выберите год поступления:"))
        self.label_5.setText(_translate("MainWindow", "Выберите курс:"))
        self.label_4.setText(_translate("MainWindow", "Выберите группу:"))
        self.label_3.setText(_translate("MainWindow", "Выберите преподавателя:"))
        self.label_2.setText(_translate("MainWindow", "Укажите путь к файлу:"))
        self.label_1.setText(_translate("MainWindow", "Выберите дисциплину:"))
        # кнопки (button)
        self.next_.setText(_translate("MainWindow", "Продолжить"))
        self.output_token.setText(_translate("MainWindow", "Билет"))
        self.gen_b.setText(_translate("MainWindow", "Сгенерировать билет"))
        self.open_pars.setText(_translate("MainWindow", "Обзор..."))
        self.pars_.setText(_translate("MainWindow", "Загрузить"))
        self.output_.setText(_translate("MainWindow", "Выгрузить"))
        # текствые поля (lineEdit)
        self.tasks_line.setText(_translate("MainWindow", "Количество заданий"))
        self.tokens_line.setText(_translate("MainWindow", "Количество билетов"))
        # чекбоксы (checkBox)
        self.checkBox_practic_out.setText(_translate("MainWindow", "Добавить практические задания"))
        self.checkBox_practic_gen.setText(_translate("MainWindow", "Добавить практические задания"))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    # глобальные переменные
    file_ = ''
    result = []
    num = 0
    practic = False

    # основаная логика приложения
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.parser = QWidget()
        self.generator_ = QWidget()
        self.output = QWidget()
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.addTab(self.parser, "Загрузка")
        self.tabWidget.addTab(self.generator_, "Генератор")
        self.tabWidget.addTab(self.output, "Выгрузка")
        self.parserUI()
        self.generatorUI()
        self.outputUI()
        self.gen_b.clicked.connect(self.NumTasksUI)
        self.next_.clicked.connect(self.generator)
        self.open_pars.clicked.connect(self.pars_win)
        self.pars_.clicked.connect(self.pars)
        self.output_.clicked.connect(self.gen_out)
        self.checkBox_practic_out.stateChanged.connect(self.clickBox)
        self.checkBox_practic_gen.stateChanged.connect(self.clickBox)
        self.showFullScreen()

    # переключение режима экрана (оконный/полноэкранный)
    def keyPressEvent(self, event):
        # если нажата клавиша F11
        if event.key() == QtCore.Qt.Key_F11:
            # если в полный экран
            if self.isFullScreen():
                # вернуть прежнее состояние
                self.showNormal()
            else:
                # иначе во весь экран
                self.showFullScreen()

    # окно парсера
    def parserUI(self):
        hlayout = QHBoxLayout(self)
        self.tabWidget = QTabWidget(self.centralwidget)
        hlayout.addWidget(self.label_2)
        hlayout.addWidget(self.filename_2)
        hlayout.addWidget(self.open_pars)
        vlayout = QVBoxLayout(self)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.pars_)
        self.tabWidget.setTabText(0, "Parser")
        self.parser.setLayout(vlayout)

    # окно генератора (переписать)
    def generatorUI(self):
        self.combo = QComboBox(self)
        cursor.execute('SELECT `name` FROM `subjects`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)):
            self.combo.addItem(check_sel[i][0])
        self.combo1 = QComboBox(self)
        cursor.execute('SELECT `name` FROM `teachers`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)):
            self.combo1.addItem(check_sel[i][0])
        self.combo2 = QComboBox(self)
        cursor.execute('SELECT `name` FROM `groups`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)):
            self.combo2.addItem(check_sel[i][0])
        self.combo3 = QComboBox(self)
        cursor.execute('SELECT `name` FROM `courses`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)):
            self.combo3.addItem(check_sel[i][0])
        self.combo4 = QComboBox(self)
        cursor.execute('SELECT `name` FROM `year_enter`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)):
            self.combo4.addItem(check_sel[i][0])
        self.combo5 = QComboBox(self)
        cursor.execute('SELECT `name` FROM `periods`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)):
            self.combo5.addItem(check_sel[i][0])
        hlayout = QHBoxLayout(self)
        self.tabWidget = QTabWidget(self.centralwidget)
        hlayout.addWidget(self.label_1)
        vlayout = QVBoxLayout(self)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.combo)
        vlayout1 = QVBoxLayout(self)
        vlayout1.addLayout(vlayout)
        vlayout1.addWidget(self.label_3)
        vlayout2 = QVBoxLayout(self)
        vlayout2.addLayout(vlayout1)
        vlayout2.addWidget(self.combo1)
        vlayout3 = QVBoxLayout(self)
        vlayout3.addLayout(vlayout2)
        vlayout3.addWidget(self.label_4)
        vlayout4 = QVBoxLayout(self)
        vlayout4.addLayout(vlayout3)
        vlayout4.addWidget(self.combo2)
        vlayout5 = QVBoxLayout(self)
        vlayout5.addLayout(vlayout4)
        vlayout5.addWidget(self.label_5)
        vlayout6 = QVBoxLayout(self)
        vlayout6.addLayout(vlayout5)
        vlayout6.addWidget(self.combo3)
        vlayout7 = QVBoxLayout(self)
        vlayout7.addLayout(vlayout6)
        vlayout7.addWidget(self.label_6)
        vlayout8 = QVBoxLayout(self)
        vlayout8.addLayout(vlayout7)
        vlayout8.addWidget(self.combo4)
        vlayout9 = QVBoxLayout(self)
        vlayout9.addLayout(vlayout8)
        vlayout9.addWidget(self.label_7)
        vlayout10 = QVBoxLayout(self)
        vlayout10.addLayout(vlayout9)
        vlayout10.addWidget(self.combo5)
        vlayout15 = QVBoxLayout(self)
        vlayout15.addLayout(vlayout10)
        vlayout15.addWidget(self.checkBox_practic_gen)
        vlayout16 = QVBoxLayout(self)
        vlayout16.addLayout(vlayout15)
        vlayout16.addWidget(self.gen_b)
        self.tabWidget.setTabText(1, "Generate")
        self.generator_.setLayout(vlayout16)

    # контроль чекбокса
    def clickBox(self, state):
        if state:
            self.practic = True
        else:
            self.practic = False

    # окно выгрузки
    def outputUI(self):
        self.combo20 = QComboBox(self)
        cursor.execute('SELECT `name` FROM `subjects`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)):
            self.combo20.addItem(check_sel[i][0])
        self.combo21 = QComboBox(self)
        cursor.execute('SELECT `name` FROM `teachers`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)):
            self.combo21.addItem(check_sel[i][0])
        self.combo22 = QComboBox(self)
        cursor.execute('SELECT `name` FROM `groups`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)):
            self.combo22.addItem(check_sel[i][0])
        self.combo23 = QComboBox(self)
        cursor.execute('SELECT `name` FROM `courses`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)):
            self.combo23.addItem(check_sel[i][0])
        self.combo24 = QComboBox(self)
        cursor.execute('SELECT `name` FROM `year_enter`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)):
            self.combo24.addItem(check_sel[i][0])
        self.combo25 = QComboBox(self)
        cursor.execute('SELECT `name` FROM `periods`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)):
            self.combo25.addItem(check_sel[i][0])
        hlayout = QHBoxLayout(self)
        self.tabWidget1 = QTabWidget(self.centralwidget)
        hlayout.addWidget(self.label_11)
        vlayout = QVBoxLayout(self)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.combo20)
        vlayout1 = QVBoxLayout(self)
        vlayout1.addLayout(vlayout)
        vlayout1.addWidget(self.label_13)
        vlayout2 = QVBoxLayout(self)
        vlayout2.addLayout(vlayout1)
        vlayout2.addWidget(self.combo21)
        vlayout3 = QVBoxLayout(self)
        vlayout3.addLayout(vlayout2)
        vlayout3.addWidget(self.label_14)
        vlayout4 = QVBoxLayout(self)
        vlayout4.addLayout(vlayout3)
        vlayout4.addWidget(self.combo22)
        vlayout5 = QVBoxLayout(self)
        vlayout5.addLayout(vlayout4)
        vlayout5.addWidget(self.label_15)
        vlayout6 = QVBoxLayout(self)
        vlayout6.addLayout(vlayout5)
        vlayout6.addWidget(self.combo23)
        vlayout7 = QVBoxLayout(self)
        vlayout7.addLayout(vlayout6)
        vlayout7.addWidget(self.label_16)
        vlayout8 = QVBoxLayout(self)
        vlayout8.addLayout(vlayout7)
        vlayout8.addWidget(self.combo24)
        vlayout9 = QVBoxLayout(self)
        vlayout9.addLayout(vlayout8)
        vlayout9.addWidget(self.label_17)
        vlayout10 = QVBoxLayout(self)
        vlayout10.addLayout(vlayout9)
        vlayout10.addWidget(self.combo25)
        vlayout15 = QVBoxLayout(self)
        vlayout15.addLayout(vlayout10)
        vlayout15.addWidget(self.checkBox_practic_out)
        hlayout1 = QHBoxLayout(self)
        hlayout1.addLayout(vlayout15)
        hlayout1.addWidget(self.label_8)
        vlayout11 = QVBoxLayout(self)
        vlayout11.addLayout(hlayout1)
        vlayout11.addWidget(self.output_)
        self.tabWidget1.setTabText(2, "Output")
        self.output.setLayout(vlayout11)

    # сам парсер
    def pars(self):
        # Чтение excel
        global file_
        file = self.file_
        df = pd.read_excel(io=file, engine='openpyxl', sheet_name='Лист1')

        # Парс excel
        result = []

        # Парс ТЕМ
        for i in range(0, len(df['Дисциплины'].tolist())):
            add_ser = 'INSERT INTO `subjects` (`name`) VALUES (%s)'
            result.append(df['Дисциплины'].tolist()[i])
            check_input = 'SELECT * FROM `subjects` WHERE `name` = %s'
            cursor.execute(check_input, result)
            if cursor.fetchone() == None:
                cursor.execute(add_ser, result)
                conn.commit()
                result = []
            else:
                result = []

        # Парс ЗАДАНИЙ
        for i in range(0, len(df['Задание'].tolist())):
            add_ser = 'INSERT INTO `tasks` (`name`) VALUES (%s)'
            result.append(df['Задание'].tolist()[i])
            check_input = 'SELECT * FROM `tasks` WHERE `name` = %s'
            cursor.execute(check_input, result)
            if cursor.fetchone() == None:
                cursor.execute(add_ser, result)
                conn.commit()
                result = []
            else:
                result = []

        # Парс ТИПОВ ЗАДАНИЙ
        for i in range(0, len(df['Тип задания'].tolist())):
            add_ser = 'INSERT INTO `type_tasks` (`name`) VALUES (%s)'
            result.append(df['Тип задания'].tolist()[i])
            check_input = 'SELECT * FROM `type_tasks` WHERE `name` = %s'
            cursor.execute(check_input, result)
            if cursor.fetchone() == None:
                cursor.execute(add_ser, result)
                conn.commit()
                result = []
            else:
                result = []

        # Парс ПРЕПОДАВАТЕЛИ
        for i in range(0, len(df['Преподаватель'].tolist())):
            add_ser = 'INSERT INTO `teachers` (`name`) VALUES (%s)'
            result.append(df['Преподаватель'].tolist()[i])
            check_input = 'SELECT * FROM `teachers` WHERE `name` = %s'
            cursor.execute(check_input, result)
            if cursor.fetchone() == None:
                cursor.execute(add_ser, result)
                conn.commit()
                result = []
            else:
                result = []

        # Парс ГРУПП
        for i in range(0, len(df['Группа'].tolist())):
            add_ser = 'INSERT INTO `groups` (`name`) VALUES (%s)'
            result.append(df['Группа'].tolist()[i])
            check_input = 'SELECT * FROM `groups` WHERE `name` = %s'
            cursor.execute(check_input, result)
            if cursor.fetchone() == None:
                cursor.execute(add_ser, result)
                conn.commit()
                result = []
            else:
                result = []

        # Парс КУСРОВ
        for i in range(0, len(df['Курс'].tolist())):
            add_ser = 'INSERT INTO `courses` (`name`) VALUES (%s)'
            result.append(df['Курс'].tolist()[i])
            check_input = 'SELECT * FROM `courses` WHERE `name` = %s'
            cursor.execute(check_input, result)
            if cursor.fetchone() == None:
                cursor.execute(add_ser, result)
                conn.commit()
                result = []
            else:
                result = []

        # Парс ГОДА ПОСТУПЛЕНИЯ
        for i in range(0, len(df['Год поступления'].tolist())):
            add_ser = 'INSERT INTO `year_enter` (`name`) VALUES (%s)'
            result.append(df['Год поступления'].tolist()[i])
            check_input = 'SELECT * FROM `year_enter` WHERE `name` = %s'
            cursor.execute(check_input, result)
            if cursor.fetchone() == None:
                cursor.execute(add_ser, result)
                conn.commit()
                result = []
            else:
                result = []

        # Парс СЕССИЙ
        for i in range(0, len(df['Сессия'].tolist())):
            add_ser = 'INSERT INTO `periods` (`name`) VALUES (%s)'
            result.append(df['Сессия'].tolist()[i])
            check_input = "SELECT * FROM `periods` WHERE `name` = %s"
            cursor.execute(check_input, result)
            if cursor.fetchone() == None:
                cursor.execute(add_ser, result)
                conn.commit()
                result = []
            else:
                result = []

        # Парс РАЗДЕЛ
        for i in range(0, len(df['Раздел'].tolist())):
            add_ser = 'INSERT INTO `blocks` (`name`) VALUES (%s)'
            result.append(df['Раздел'].tolist()[i])
            check_input = 'SELECT * FROM `blocks` WHERE `name` = %s'
            cursor.execute(check_input, result)
            if cursor.fetchone() == None:
                cursor.execute(add_ser, result)
                conn.commit()
                result = []
            else:
                result = []
        # Парс БИЛЕТОВ
        for i in range(0, len(df['Дисциплины'].tolist())):
            add_ser = 'INSERT INTO `tokens` (`subjects_id`, `tasks_id`, `blocks_id`, `type_tasks_id`, `teachers_id`, ' \
                      '`groups_id`, `courses_id`, `year_enter_id`, periods_id) ' \
                      'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            for j in range(0, len(df.values.tolist()[i])):
                data_db = []
                if j == 0:
                    data_db.append(df.values.tolist()[i][j])
                    check_input = 'SELECT `id` FROM `subjects` WHERE `name` = %s'
                    cursor.execute(check_input, data_db)
                    result.append(cursor.fetchone()[0])
                elif j == 1:
                    data_db.append(df.values.tolist()[i][j])
                    check_input = 'SELECT `id` FROM `tasks` WHERE `name` = %s'
                    cursor.execute(check_input, data_db)
                    result.append(cursor.fetchone()[0])
                elif j == 2:
                    data_db.append(df.values.tolist()[i][j])
                    check_input = 'SELECT `id` FROM `blocks` WHERE `name` = %s'
                    cursor.execute(check_input, data_db)
                    result.append(cursor.fetchone()[0])
                elif j == 3:
                    data_db.append(df.values.tolist()[i][j])
                    check_input = 'SELECT `id` FROM `type_tasks` WHERE `name` = %s'
                    cursor.execute(check_input, data_db)
                    result.append(cursor.fetchone()[0])
                elif j == 4:
                    data_db.append(df.values.tolist()[i][j])
                    check_input = 'SELECT `id` FROM `teachers` WHERE `name` = %s'
                    cursor.execute(check_input, data_db)
                    result.append(cursor.fetchone()[0])
                elif j == 5:
                    data_db.append(df.values.tolist()[i][j])
                    check_input = 'SELECT `id` FROM `groups` WHERE `name` = %s'
                    cursor.execute(check_input, data_db)
                    result.append(cursor.fetchone()[0])
                elif j == 6:
                    data_db.append(df.values.tolist()[i][j])
                    check_input = 'SELECT `id` FROM `courses` WHERE `name` = %s'
                    cursor.execute(check_input, data_db)
                    result.append(cursor.fetchone()[0])
                elif j == 7:
                    data_db.append(df.values.tolist()[i][j])
                    check_input = 'SELECT `id` FROM `year_enter` WHERE `name` = %s'
                    cursor.execute(check_input, data_db)
                    result.append(cursor.fetchone()[0])
                elif j == 8:
                    data_db.append(df.values.tolist()[i][j])
                    check_input = 'SELECT `id` FROM `periods` WHERE `name` = %s'
                    cursor.execute(check_input, data_db)
                    result.append(cursor.fetchone()[0])
            check_input = 'SELECT * FROM `tokens` WHERE `subjects_id` = %s AND `tasks_id` = %s AND `blocks_id` = %s ' \
                          'AND `type_tasks_id` = %s AND `teachers_id` = %s AND `groups_id` = %s ' \
                          'AND `courses_id` = %s AND `year_enter_id` = %s AND `periods_id` = %s'
            cursor.execute(check_input, result)
            if cursor.fetchone() == None:
                cursor.execute(add_ser, result)
                conn.commit()
                result = []
            else:
                result = []

    # проверка админ прав
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:

            return False

    # диалоговое окно
    def pars_win(self):
        self.open_pars.hide()
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './', '(*.xls *.xlsx)')
        if fname:
            global file_
            self.filename_2.setText(fname)
            self.file_ += str(fname)
        # if self.is_admin():
        #     fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './', '(*.xls *.xlsx)')
        #     if fname:
        #         global file_
        #         self.filename_2.setText(fname)
        #         self.file_ += str(fname)
        # else:
        #     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

    # вывод билетов
    def gen_out(self):
        global result
        global num
        doc = aw.Document()
        builder = aw.DocumentBuilder(doc)
        for i in range(0, len(self.result)):
            builder.writeln("Дисциплина: " + str(self.result[i][0]))
            builder.writeln("Преподаватель: " + str(self.result[i][1]))
            builder.writeln("Группа: " + str(self.result[i][2]))
            builder.writeln("Курс: " + str(self.result[i][3]))
            builder.writeln("Год поступления: " + str(self.result[i][4]))
            builder.writeln("Период: " + str(self.result[i][5]))
            builder.writeln("Тип работы: " + str(self.result[i][6]))
            builder.writeln("Раздел: " + str(self.result[i][7]))
            builder.writeln("Задание: " + str(self.result[i][8]))
        self.num += 1
        text, ok = QInputDialog.getText(self, 'Введите название каталога', 'Название каталога (папки)')
        if ok:
            self.folder_name = str(text)
            os.mkdir(str(text))
        doc.save('/' + str(self.folder_name) + '/' + 'Билет № ' + str(self.num) + '.docx')
        self.label_8.setText('/' + str(self.folder_name) + '/' + 'Билет № ' + str(self.num) + '.docx')

    # сам генератор
    def generator(self):
        global result
        res = []
        type_t = []
        cursor.execute('SELECT `id`, `name` FROM `subjects`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)+1):
            if str(check_sel[i][1]) == str(self.combo.currentText()):
                res.append(check_sel[i][0])
                break
        cursor.execute('SELECT `id`, `name` FROM `teachers`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)+1):
            if check_sel[i][1] == self.combo1.currentText():
                res.append(check_sel[i][0])
                break
        cursor.execute('SELECT `id`, `name` FROM `groups`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)+1):
            if check_sel[i][1] == self.combo2.currentText():
                res.append(check_sel[i][0])
                break
        cursor.execute('SELECT `id`, `name` FROM `courses`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)+1):
            if check_sel[i][1] == self.combo3.currentText():
                res.append(check_sel[i][0])
                break
        cursor.execute('SELECT `id`, `name` FROM `year_enter`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)+1):
            if str(check_sel[i][1]) == str(self.combo4.currentText()):
                res.append(check_sel[i][0])
                break
        cursor.execute('SELECT `id`, `name` FROM `periods`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)+1):
            if check_sel[i][1] == self.combo5.currentText():
                res.append(check_sel[i][0])
                break

        type_t.append(res[0])
        type_t.append(res[1])
        type_t.append(res[2])
        type_t.append(res[3])
        type_t.append(res[4])
        type_t.append(res[5])
        block_list_id = []
        id_block = 'SELECT DISTINCT `blocks_id` FROM `tokens` WHERE subjects_id = %s ' \
             'AND teachers_id = %s AND groups_id = %s AND courses_id = %s AND year_enter_id = %s ' \
             'AND periods_id = %s'
        cursor.execute(id_block, type_t)
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel)):
            block_list_id.append(check_sel[i][0])
        count_tasks_to_block = []
        count_tasks_to_block.append(type_t[0])
        count_tasks_to_block.append(type_t[1])
        count_tasks_to_block.append(type_t[2])
        count_tasks_to_block.append(type_t[3])
        count_tasks_to_block.append(type_t[4])
        count_tasks_to_block.append(type_t[5])
        cursor.execute("SELECT `id` FROM type_tasks WHERE `name` = 'теория'")
        count_tasks_to_block.append(cursor.fetchone()[0])
        count_tasks_to_block.append(0)
        check_blocks_teor = []
        for i in range(0, len(block_list_id)):
            count_tasks_to_block[7] = block_list_id[i]
            sel_check_blocks_teor = 'SELECT count(blocks_id) FROM tokens WHERE subjects_id = %s AND teachers_id = %s ' \
                                    'AND groups_id = %s AND courses_id = %s AND year_enter_id = %s AND periods_id = %s ' \
                                    'AND type_tasks_id = %s AND blocks_id = %s'
            cursor.execute(sel_check_blocks_teor, count_tasks_to_block)
            check_blocks_teor.append(cursor.fetchone()[0])
        cursor.execute("SELECT `id` FROM type_tasks WHERE `name` = 'практика'")
        count_tasks_to_block[6] = cursor.fetchone()[0]
        check_blocks_pract = []
        for i in range(0, len(block_list_id)):
            count_tasks_to_block[7] = block_list_id[i]
            sel_check_blocks_pract = 'SELECT count(blocks_id) FROM tokens WHERE subjects_id = %s AND teachers_id = %s ' \
                                    'AND groups_id = %s AND courses_id = %s AND year_enter_id = %s AND periods_id = %s ' \
                                    'AND type_tasks_id = %s AND blocks_id = %s'
            cursor.execute(sel_check_blocks_pract, count_tasks_to_block)
            check_blocks_pract.append(cursor.fetchone()[0])
        set_ = 0
        minimal = int(check_blocks_teor[0])
        for i in range(0, len(check_blocks_teor)):
            if int(check_blocks_teor[i]) < (int(self.tokens_line.text())*int(self.num_blocks_t[i])):
                if set_ < math.ceil((int(self.tokens_line.text())*int(self.num_blocks_t[i]))/int(check_blocks_teor[i])):
                    set_ = math.ceil((int(self.tokens_line.text())*int(self.num_blocks_t[i]))/int(check_blocks_teor[i]))

        if self.practic == True:
            for i in range(0, len(check_blocks_pract)):
                if int(check_blocks_pract[i]) < (int(self.tokens_line.text())*int(self.num_blocks_p[i])):
                    if set_ < math.ceil((int(self.tokens_line.text())*int(self.num_blocks_p[i]))/int(check_blocks_pract[i])):
                        set_ = math.ceil((int(self.tokens_line.text())*int(self.num_blocks_p[i]))/int(check_blocks_pract[i]))
                if minimal < int(check_blocks_teor[i])+int(check_blocks_pract[i])/int(self.num_blocks_t[i])+int(self.num_blocks_p[i]):
                    minimal = int(check_blocks_teor[i])+int(check_blocks_pract[i])/int(self.num_blocks_t[i])+int(self.num_blocks_p[i])
        else:
            for i in range(0, len(check_blocks_teor)):
                if minimal < int(check_blocks_teor[i]) / int(self.num_blocks_t[i]):
                    minimal = int(check_blocks_teor[i]) / int(self.num_blocks_t[i])
        sum_p = sum(self.num_blocks_p)
        sum_t = sum(self.num_blocks_t)
        sum_all = sum_p + sum_t
        arr_tok = []
        for i in range(0, set_):
            if sum_all >= minimal:
                arr_tok.append(minimal)
                sum_all -= minimal
            else:
                arr_tok.append(sum_all)
        type_t.append(0)
        type_t.append(0)
        if set_ == 0:
            set_ += 1
        num_token = 0
        if len(arr_tok) == 0:
            arr_tok.append(int(self.tokens_line.text()))
        for q in range(1, set_+1):
            for m in range(1, arr_tok[q-1]+1):
                num_token += 1
                set_q = []
                set_q.append(q)
                sel_set = 'SELECT `tokens_id`, `set` FROM `exam_tokens` WHERE `set` = %s'
                cursor.execute(sel_set, set_q)
                check_token = cursor.fetchall()
                ct_id = []
                ct_set = []
                if check_token != None:
                    for k in range(0, len(check_token)):
                        ct_id.append(check_token[k][0])
                    for y in range(0, len(check_token)):
                        ct_set.append(check_token[y][1])
                for i in range(0, len(block_list_id)):
                    cursor.execute("SELECT `id` FROM `type_tasks` WHERE `name` = 'теория'")
                    sel_teor = cursor.fetchone()
                    type_t[6] = sel_teor[0]
                    write = 0
                    type_t[7] = block_list_id[i]
                    type_task_id = []
                    id_teor = 'SELECT `id` FROM `tokens` ' \
                                 'WHERE `subjects_id` = %s AND `teachers_id` = %s ' \
                                 'AND `groups_id` = %s AND `courses_id` = %s ' \
                                 'AND `year_enter_id` = %s AND `periods_id` = %s ' \
                                 'AND `type_tasks_id` = %s AND `blocks_id` = %s'
                    cursor.execute(id_teor, type_t)
                    check_teor = cursor.fetchall()
                    for j in range(0, len(check_teor)):
                        if check_teor[j][0] not in ct_id and q not in ct_set:
                            type_task_id.append(check_teor[j][0])
                    while write != int(self.num_blocks_t[i]):
                        task = random.randint(0, len(type_task_id)-1)
                        all_id_in_token = [0 for x in range(0, len(type_t))]
                        all_id_in_token[0] = type_t[0]
                        all_id_in_token[1] = type_t[1]
                        all_id_in_token[2] = type_t[2]
                        all_id_in_token[3] = type_t[3]
                        all_id_in_token[4] = type_t[4]
                        all_id_in_token[5] = type_t[5]
                        all_id_in_token[6] = type_t[6]
                        all_id_in_token[7] = type_t[7]
                        all_id_in_token.append(type_task_id[task])
                        sel_name_of_objects = 'SELECT ' \
                                              '(SELECT `name` FROM `subjects` WHERE id = %s), ' \
                                              '(SELECT `name` FROM `teachers` WHERE id = %s), ' \
                                              '(SELECT `name` FROM `groups` WHERE id = %s), ' \
                                              '(SELECT `name` FROM `courses` WHERE id = %s), ' \
                                              '(SELECT `name` FROM `year_enter` WHERE id = %s), ' \
                                              '(SELECT `name` FROM `periods` WHERE id = %s), ' \
                                              '(SELECT `name` FROM `type_tasks` WHERE id = %s), ' \
                                              '(SELECT `name` FROM `blocks` WHERE id = %s),' \
                                              '(SELECT `name` FROM `tasks` WHERE id = %s) ' \
                                              'FROM `tokens`'
                        cursor.execute(sel_name_of_objects, all_id_in_token)
                        search_data = cursor.fetchone()
                        type_task_id.pop(task)
                        write += 1
                        sel_id_token = 'SELECT `id` FROM `tokens` WHERE `subjects_id` = %s AND `teachers_id` = %s AND ' \
                                       '`groups_id` = %s AND `courses_id` = %s AND `year_enter_id` = %s AND ' \
                                       '`periods_id` = %s AND `type_tasks_id` = %s ' \
                                       'AND `blocks_id` = %s AND `tasks_id` = %s'
                        cursor.execute(sel_id_token, all_id_in_token)
                        id_token = cursor.fetchone()[0]
                        # Чтение excel
                        file = 'exam.xlsx'
                        df = pd.read_excel(io=file, engine='openpyxl', sheet_name='Лист1')
                        for w in range(0, len(df['Дисциплины'].tolist())):
                            if str(search_data[0]) in df.values.tolist()[w]:
                                if str(search_data[1]) in df.values.tolist()[w]:
                                    if str(search_data[2]) in df.values.tolist()[w]:
                                        if int(search_data[3]) in df.values.tolist()[w]:
                                            if int(search_data[4]) in df.values.tolist()[w]:
                                                if str(search_data[5]) in df.values.tolist()[w]:
                                                    date = df.values.tolist()[w][6]
                                                    break
                        input_exam_tokens = 'INSERT INTO `exam_tokens` (`number`, `tokens_id`, `date_exam`, `set`) ' \
                                            'VALUES (%s, %s, %s, %s)'
                        exam_token = []
                        exam_token.append(num_token)
                        exam_token.append(id_token)
                        exam_token.append(date)
                        exam_token.append(q)
                        cursor.execute(input_exam_tokens, exam_token)
                        conn.commit()
                    if self.practic == True:
                        cursor.execute("SELECT `id` FROM `type_tasks` WHERE `name` = 'практика'")
                        sel_practic = cursor.fetchone()
                        type_t[6] = sel_practic[0]
                        type_task_id = []
                        id_teor = 'SELECT `id` FROM `tokens` ' \
                                     'WHERE `subjects_id` = %s AND `teachers_id` = %s ' \
                                     'AND `groups_id` = %s AND `courses_id` = %s ' \
                                     'AND `year_enter_id` = %s AND `periods_id` = %s ' \
                                     'AND `type_tasks_id` = %s AND `blocks_id` = %s'
                        cursor.execute(id_teor, type_t)
                        check_teor = cursor.fetchall()
                        write = 0
                        for j in range(0, len(check_teor)):
                            if check_teor[j][0] not in ct_id and q not in ct_set:
                                type_task_id.append(check_teor[j][0])
                        while write != int(self.num_blocks_p[i]):
                            task = random.randint(0, len(type_task_id) - 1)
                            all_id_in_token = [0 for x in range(0, len(type_t))]
                            all_id_in_token[0] = type_t[0]
                            all_id_in_token[1] = type_t[1]
                            all_id_in_token[2] = type_t[2]
                            all_id_in_token[3] = type_t[3]
                            all_id_in_token[4] = type_t[4]
                            all_id_in_token[5] = type_t[5]
                            all_id_in_token[6] = type_t[6]
                            all_id_in_token[7] = type_t[7]
                            all_id_in_token.append(type_task_id[task])
                            sel_name_of_objects = 'SELECT ' \
                                                  '(SELECT `name` FROM `subjects` WHERE id = %s), ' \
                                                  '(SELECT `name` FROM `teachers` WHERE id = %s), ' \
                                                  '(SELECT `name` FROM `groups` WHERE id = %s), ' \
                                                  '(SELECT `name` FROM `courses` WHERE id = %s), ' \
                                                  '(SELECT `name` FROM `year_enter` WHERE id = %s), ' \
                                                  '(SELECT `name` FROM `periods` WHERE id = %s), ' \
                                                  '(SELECT `name` FROM `type_tasks` WHERE id = %s), ' \
                                                  '(SELECT `name` FROM `blocks` WHERE id = %s), ' \
                                                  '(SELECT `name` FROM `tasks` WHERE id = %s) ' \
                                                  'FROM `tokens`'
                            cursor.execute(sel_name_of_objects, all_id_in_token)
                            search_data = cursor.fetchone()
                            sel_id_token = 'SELECT `id` FROM `tokens` WHERE `subjects_id` = %s AND `teachers_id` = %s AND ' \
                                           '`groups_id` = %s AND `courses_id` = %s AND `year_enter_id` = %s AND ' \
                                           '`periods_id` = %s AND `type_tasks_id` = %s ' \
                                           'AND `blocks_id` = %s AND `tasks_id` = %s'
                            cursor.execute(sel_id_token, all_id_in_token)
                            id_token = cursor.fetchone()[0]
                            # Чтение excel
                            file = 'exam.xlsx'
                            df = pd.read_excel(io=file, engine='openpyxl', sheet_name='Лист1')
                            for w in range(0, len(df['Дисциплины'].tolist())):
                                if str(search_data[0]) in df.values.tolist()[w]:
                                    if str(search_data[1]) in df.values.tolist()[w]:
                                        if str(search_data[2]) in df.values.tolist()[w]:
                                            if int(search_data[3]) in df.values.tolist()[w]:
                                                if int(search_data[4]) in df.values.tolist()[w]:
                                                    if str(search_data[5]) in df.values.tolist()[w]:
                                                        date = df.values.tolist()[w][6]
                                                        break
                            input_exam_tokens = 'INSERT INTO `exam_tokens` (`number`, `tokens_id`, `date_exam`, `set`) ' \
                                                'VALUES (%s, %s, %s, %s)'
                            exam_token = []
                            exam_token.append(num_token)
                            exam_token.append(id_token)
                            exam_token.append(date)
                            exam_token.append(q)
                            cursor.execute(input_exam_tokens, exam_token)
                            conn.commit()
                            type_task_id.pop(task)
                            write += 1

    # проверка введённого кол-ва заданий
    def NumTasksUI(self):
        sel_ob_id = 'SELECT `id` FROM `subjects` WHERE `name` = %s'
        ob_id = []
        ob_id.append(self.combo.currentText())
        cursor.execute(sel_ob_id, ob_id)
        blocks_id = []
        blocks_id.append(cursor.fetchone()[0])
        sel_ob_id = 'SELECT `id` FROM `teachers` WHERE `name` = %s'
        ob_id = []
        ob_id.append(self.combo1.currentText())
        cursor.execute(sel_ob_id, ob_id)
        blocks_id.append(cursor.fetchone()[0])
        sel_ob_id = 'SELECT `id` FROM `groups` WHERE `name` = %s'
        ob_id = []
        ob_id.append(self.combo2.currentText())
        cursor.execute(sel_ob_id, ob_id)
        blocks_id.append(cursor.fetchone()[0])
        sel_ob_id = 'SELECT `id` FROM `courses` WHERE `name` = %s'
        ob_id = []
        ob_id.append(self.combo3.currentText())
        cursor.execute(sel_ob_id, ob_id)
        blocks_id.append(cursor.fetchone()[0])
        sel_ob_id = 'SELECT `id` FROM `year_enter` WHERE `name` = %s'
        ob_id = []
        ob_id.append(self.combo4.currentText())
        cursor.execute(sel_ob_id, ob_id)
        blocks_id.append(cursor.fetchone()[0])
        sel_ob_id = 'SELECT `id` FROM `periods` WHERE `name` = %s'
        ob_id = []
        ob_id.append(self.combo5.currentText())
        cursor.execute(sel_ob_id, ob_id)
        blocks_id.append(cursor.fetchone()[0])
        sel_blocks_id = 'SELECT DISTINCT blocks_id FROM `tokens` WHERE `subjects_id` = %s AND `teachers_id` = %s AND ' \
                        '`groups_id` = %s AND `courses_id` = %s AND `year_enter_id` = %s AND `periods_id` = %s'
        cursor.execute(sel_blocks_id, blocks_id)
        self.result_blocks_id = cursor.fetchall()
        self.blocks_arr = []
        self.num_blocks_t = []
        self.num_blocks_p = []
        for i in range(0, len(self.result_blocks_id)):
            sel_name_blocks = 'SELECT `name` FROM `blocks` WHERE id = %s'
            bl_id = []
            bl_id.append(self.result_blocks_id[i][0])
            cursor.execute(sel_name_blocks, bl_id)
            self.blocks_arr.append(cursor.fetchone()[0])
        text, ok = QInputDialog.getText(self, 'Количество билетов', 'Количество билетов')
        if ok:
            self.tokens_line.setText(str(text))
        for i in range(0, len(self.blocks_arr)):
            text, ok = QInputDialog.getText(self, 'Количество заданий', 'Количество теоретических заданий из раздела: ' + str(self.blocks_arr[i]))
            if ok:
                self.num_blocks_t.append(int(text))
                self.tasks_line.setText(str(text))
        if self.practic == True:
            for i in range(0, len(self.blocks_arr)):
                text, ok = QInputDialog.getText(self, 'Количество заданий', 'Количество приктических заданий из раздела: ' + str(self.blocks_arr[i]))
                if ok:
                    self.num_blocks_p.append(int(text))
                    self.tasks_line.setText(str(text))
        blocks_id.append(0)
        blocks_id.append(0)
        right = True
        for i in range(0, len(self.result_blocks_id)-1):
            cursor.execute("SELECT `id` FROM `type_tasks` WHERE `name` = 'теория'")
            blocks_id[6] = self.result_blocks_id[i][0]
            blocks_id[7] = cursor.fetchone()[0]
            sel_count_tasks = "SELECT COUNT(`id`) FROM `tokens` WHERE `subjects_id` = %s AND `teachers_id` = %s AND " \
                        "`groups_id` = %s AND `courses_id` = %s AND `year_enter_id` = %s AND `periods_id` = %s AND " \
                        "`blocks_id` = %s AND `type_tasks_id` = %s"
            cursor.execute(sel_count_tasks, blocks_id)
            count_ = cursor.fetchone()[0]
            if self.practic == True:
                if count_ < (int(self.num_blocks_p[i])*int(self.tokens_line.text())):
                    self.dlg = QMessageBox()
                    self.dlg.addButton("Да", QMessageBox.AcceptRole)
                    self.dlg.addButton("Нет", QMessageBox.AcceptRole)
                    self.dlg.setIcon(QMessageBox.Information)
                    self.dlg.setWindowTitle("Сохранение")
                    number = (int(self.num_blocks_p[i])*int(self.tokens_line.text())) - int(count_)
                    self.dlg.setInformativeText(
                        "Не хватает " + str(number) + " вопросов для генерации билетов! Всё равно сгенерировать?")
                    bttn = self.dlg.exec()
                    if self.dlg.clickedButton().text() == "Нет":
                        right = False
                        break
                if right == True:
                    cursor.execute("SELECT `id` FROM `type_tasks` WHERE `name` = 'практика'")
                    blocks_id[7] = cursor.fetchone()[0]
                    sel_count_tasks = "SELECT COUNT(`id`) FROM `tokens` WHERE `subjects_id` = %s AND `teachers_id` = %s AND " \
                                      "`groups_id` = %s AND `courses_id` = %s AND `year_enter_id` = %s AND `periods_id` = %s AND " \
                                      "`blocks_id` = %s AND `type_tasks_id` = %s"
                    cursor.execute(sel_count_tasks, blocks_id)
                    count_ = cursor.fetchone()[0]
                    if count_ < (int(self.num_blocks_p[i]) * int(self.tokens_line.text())):
                        self.dlg = QMessageBox()
                        self.dlg.addButton("Да", QMessageBox.AcceptRole)
                        self.dlg.addButton("Нет", QMessageBox.AcceptRole)
                        self.dlg.setIcon(QMessageBox.Information)
                        self.dlg.setWindowTitle("Сохранение")
                        number = (int(self.num_blocks_p[i]) * int(self.tokens_line.text())) - int(count_)
                        self.dlg.setInformativeText(
                            "Не хватает " + str(number) + " вопросов для генерации билетов! Всё равно сгенерировать?")
                        bttn = self.dlg.exec()
                        if self.dlg.clickedButton().text() == "Нет":
                            right = False
                            break

        self.dlg = QMessageBox()
        self.dlg.addButton("Да", QMessageBox.AcceptRole)
        self.dlg.addButton("Нет", QMessageBox.AcceptRole)
        self.dlg.setIcon(QMessageBox.Information)
        self.dlg.setWindowTitle("Генерация")
        self.dlg.setInformativeText(
            "Начать генерацию экзаменационных билетов?")
        bttn = self.dlg.exec()
        if self.dlg.clickedButton().text() == "Да":
            self.generator()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

#++++++++++++++++++++++++++++++++++++++++++++++++++
'''
Выгрузку всего и вообще посмотреть что там с выгрузкой!!!
Учётки
CRUD
'''
