import pandas as pd
import mysql.connector
import random
import aspose.words as aw
import ctypes, sys
import os, os.path
import math
import json
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
        self.signup_btn = QPushButton(Login)
        self.signup_btn.setGeometry(QRect(290, 200, 51, 23))
        self.signup_btn.setObjectName("signup_btn")
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
        hl2.addWidget(self.signup_btn)
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
        self.signup_btn.setText(_translate("Login", "Зарегистрировать"))
        self.label.setText(_translate("Login", "Логин"))
        self.label1.setText(_translate("Login", "Пароль"))


class Login(QtWidgets.QDialog, Ui_Login):
    # основная логика окна
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setupUi(self)
        self.login_btn.clicked.connect(self.loginCheck)
        self.signup_btn.clicked.connect(self.signUpCheck)

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
        self.show()

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


class Ui_UpdateQuestion(QtWidgets.QWidget):
    def setupUi(self, UpdateQuestion):
        UpdateQuestion.setObjectName("UpdateQuestion")
        UpdateQuestion.resize(496, 265)
        self.update_btn = QtWidgets.QPushButton(UpdateQuestion)
        self.update_btn.setGeometry(QRect(230, 200, 51, 23))
        self.update_btn.setObjectName("update_btn")
        self.retranslateUi(UpdateQuestion)
        QtCore.QMetaObject.connectSlotsByName(UpdateQuestion)

    def retranslateUi(self, UpdateQuestion):
        _translate = QCoreApplication.translate
        UpdateQuestion.setWindowTitle(_translate("UpdateQuestion", "Редактирование"))
        self.update_btn.setText(_translate("UpdateQuestion", "Редактировать"))


class UpdateQuestion(QtWidgets.QDialog, Ui_UpdateQuestion):
    def __init__(self, data, users, parent=None):
        sub_name = []
        tea_name = []
        gr_name = []
        cour_name = []
        ye_name = []
        per_name = []
        tt_name = []
        bl_name = []
        sub_name.append(data[0])
        tea_name.append(data[1])
        gr_name.append(data[2])
        cour_name.append(data[3])
        ye_name.append(data[4])
        per_name.append(data[5])
        tt_name.append(data[6])
        bl_name.append(data[7])
        id_data = []
        sel_sub = 'SELECT `id` FROM `subjects` WHERE `name` = %s'
        cursor.execute(sel_sub, sub_name)
        id_data.append(cursor.fetchone()[0])
        sel_tea = 'SELECT `id` FROM `teachers` WHERE `name` = %s'
        cursor.execute(sel_tea, tea_name)
        id_data.append(cursor.fetchone()[0])
        sel_gr = 'SELECT `id` FROM `groups` WHERE `name` = %s'
        cursor.execute(sel_gr, gr_name)
        id_data.append(cursor.fetchone()[0])
        sel_cour = 'SELECT `id` FROM `courses` WHERE `name` = %s'
        cursor.execute(sel_cour, cour_name)
        id_data.append(cursor.fetchone()[0])
        sel_ye = 'SELECT `id` FROM `year_enter` WHERE `name` = %s'
        cursor.execute(sel_ye, ye_name)
        id_data.append(cursor.fetchone()[0])
        sel_per = 'SELECT `id` FROM `periods` WHERE `name` = %s'
        cursor.execute(sel_per, per_name)
        id_data.append(cursor.fetchone()[0])
        sel_tt = 'SELECT `id` FROM `type_tasks` WHERE `name` = %s'
        cursor.execute(sel_tt, tt_name)
        id_data.append(cursor.fetchone()[0])
        sel_bl = 'SELECT `id` FROM `blocks` WHERE `name` = %s'
        cursor.execute(sel_bl, bl_name)
        id_data.append(cursor.fetchone()[0])
        main_id = []
        sel_main_id = 'SELECT `id` FROM `tokens` WHERE `subjects_id` = %s AND `teachers_id` = %s AND `groups_id` = %s AND ' \
                      '`courses_id` = %s AND `year_enter_id` = %s AND `periods_id` = %s AND `type_tasks_id` = %s AND ' \
                      '`blocks_id` = %s'
        cursor.execute(sel_main_id, id_data)
        id_ = cursor.fetchall()
        for i in range(0, len(id_)):
            main_id.append(id_[i][0])
        super(UpdateQuestion, self).__init__(parent)
        self.setupUi(self)
        self.update_btn.clicked.connect(self.update_token)
        vopr_id = []
        for i in range(0, len(main_id)):
            id_ = []
            id_.append(main_id[i])
            sel_vopr = 'SELECT * FROM `tokens` WHERE `id` = %s'
            cursor.execute(sel_vopr, id_)
            vopr_id.append(cursor.fetchall()[0])
        self.table = QTableWidget(self)
        self.table.setColumnCount(len(vopr_id[0]))
        self.table.setRowCount(len(vopr_id))
        self.table.setHorizontalHeaderLabels(
            ["Номер", "Дисциплина", "Задание", "Тип задания", "Преподаватель", "Группа",
             "Курсы", "Год поступления", "Период", "Раздел"])
        for i in range(0, len(vopr_id)):
            v_id = []
            v_id.append(vopr_id[i][0])
            v_id.append(vopr_id[i][1])
            v_id.append(vopr_id[i][2])
            v_id.append(vopr_id[i][3])
            v_id.append(vopr_id[i][4])
            v_id.append(vopr_id[i][5])
            v_id.append(vopr_id[i][6])
            v_id.append(vopr_id[i][7])
            v_id.append(vopr_id[i][8])
            v_id.append(vopr_id[i][9])
            sel_vopr_name = 'SELECT ' \
                            '(SELECT `id` FROM `tokens` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `subjects` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `tasks` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `type_tasks` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `teachers` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `groups` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `courses` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `year_enter` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `periods` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `blocks` WHERE `id` = %s) ' \
                            'FROM `tokens`'
            cursor.execute(sel_vopr_name, v_id)
            vopr = cursor.fetchone()
            for j in range(0, len(vopr)):
                if j == 0:
                    item = QTableWidgetItem(str(vopr[j]))
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.table.setItem(i, j, item)
                elif j == 4 and users[4] != None:
                    item = QTableWidgetItem(str(vopr[j]))
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.table.setItem(i, j, item)
                else:
                    self.table.setItem(i, j, QTableWidgetItem(str(vopr[j])))
        vlayout = QVBoxLayout(self)
        vlayout.addWidget(self.table)
        vlayout.addWidget(self.update_btn)

    def update_token(self):
        for i in range(self.table.rowCount()):
            tb_data = []
            for j in range(0, self.table.columnCount()):
                tb_data.append(self.table.item(i, j).text())
            check_sub = 'SELECT * FROM `subjects` WHERE `name` = %s'
            sub_name = []
            sub_name.append(tb_data[1])
            cursor.execute(check_sub, sub_name)
            sub_id = cursor.fetchone()
            if sub_id == None:
                in_sub = 'INSERT INTO `subjects` (`name`) VALUES (%s)'
                cursor.execute(in_sub, sub_name)
                conn.commit()
            check_tas = 'SELECT * FROM `tasks` WHERE `name` = %s'
            tas_name = []
            tas_name.append(tb_data[2])
            cursor.execute(check_tas, tas_name)
            tas_id = cursor.fetchone()
            if tas_id == None:
                in_tas = 'INSERT INTO `tasks` (`name`) VALUES (%s)'
                cursor.execute(in_tas, tas_name)
                conn.commit()
            check_tea = 'SELECT * FROM `teachers` WHERE `name` = %s'
            tea_name = []
            tea_name.append(tb_data[4])
            cursor.execute(check_tea, tea_name)
            tea_id = cursor.fetchone()
            if tea_id == None:
                in_tea = 'INSERT INTO `teachers` (`name`) VALUES (%s)'
                cursor.execute(in_tea, tea_name)
                conn.commit()
            check_gr = 'SELECT * FROM `groups` WHERE `name` = %s'
            gr_name = []
            gr_name.append(tb_data[5])
            cursor.execute(check_gr, gr_name)
            gr_id = cursor.fetchone()
            if gr_id == None:
                in_gr = 'INSERT INTO `groups` (`name`) VALUES (%s)'
                cursor.execute(in_gr, gr_name)
                conn.commit()
            check_cour = 'SELECT * FROM `courses` WHERE `name` = %s'
            cour_name = []
            cour_name.append(tb_data[6])
            cursor.execute(check_cour, cour_name)
            cour_id = cursor.fetchone()
            if cour_id == None:
                in_cour = 'INSERT INTO `courses` (`name`) VALUES (%s)'
                cursor.execute(in_cour, cour_name)
                conn.commit()
            check_ye = 'SELECT * FROM `year_enter` WHERE `name` = %s'
            ye_name = []
            ye_name.append(tb_data[7])
            cursor.execute(check_ye, ye_name)
            ye_id = cursor.fetchone()
            if ye_id == None:
                in_ye = 'INSERT INTO `year_enter` (`name`) VALUES (%s)'
                cursor.execute(in_ye, ye_name)
                conn.commit()
            check_per = 'SELECT * FROM `periods` WHERE `name` = %s'
            per_name = []
            per_name.append(tb_data[8])
            cursor.execute(check_per, per_name)
            per_id = cursor.fetchone()
            if per_id == None:
                in_per = 'INSERT INTO `periods` (`name`) VALUES (%s)'
                cursor.execute(in_per, per_name)
                conn.commit()
            check_bl = 'SELECT * FROM `blocks` WHERE `name` = %s'
            bl_name = []
            bl_name.append(tb_data[9])
            cursor.execute(check_bl, bl_name)
            bl_id = cursor.fetchone()
            if bl_id == None:
                in_bl = 'INSERT INTO `blocks` (`name`) VALUES (%s)'
                cursor.execute(in_bl, bl_name)
                conn.commit()
            sel_id = 'SELECT ' \
                    '(SELECT `id` FROM `tokens` WHERE `id` = %s), ' \
                    '(SELECT `id` FROM `subjects` WHERE `name` = %s), ' \
                    '(SELECT `id` FROM `tasks` WHERE `name` = %s), ' \
                    '(SELECT `id` FROM `type_tasks` WHERE `name` = %s), ' \
                    '(SELECT `id` FROM `teachers` WHERE `name` = %s), ' \
                    '(SELECT `id` FROM `groups` WHERE `name` = %s), ' \
                    '(SELECT `id` FROM `courses` WHERE `name` = %s), ' \
                    '(SELECT `id` FROM `year_enter` WHERE `name` = %s), ' \
                    '(SELECT `id` FROM `periods` WHERE `name` = %s), ' \
                    '(SELECT `id` FROM `blocks` WHERE `name` = %s) ' \
                    'FROM `tokens`'
            cursor.execute(sel_id, tb_data)
            id_data = cursor.fetchone()
            check_db = 'SELECT * FROM `tokens` WHERE `id` = %s AND `subjects_id` = %s AND `tasks_id` = %s AND ' \
                       '`type_tasks_id` = %s AND `teachers_id` = %s AND `groups_id` = %s AND `courses_id` = %s AND ' \
                       '`year_enter_id` = %s AND `periods_id` = %s AND `blocks_id` = %s'
            cursor.execute(check_db, id_data)
            check_ = cursor.fetchone()
            if check_ == None:
                up_id = []
                up_id.append(id_data[1])
                up_id.append(id_data[2])
                up_id.append(id_data[3])
                up_id.append(id_data[4])
                up_id.append(id_data[5])
                up_id.append(id_data[6])
                up_id.append(id_data[7])
                up_id.append(id_data[8])
                up_id.append(id_data[9])
                up_id.append(id_data[0])
                up_t = 'UPDATE `tokens` SET `subjects_id` = %s, `tasks_id` = %s, `type_tasks_id` = %s, ' \
                       '`teachers_id` = %s, `groups_id` = %s, `courses_id` = %s, `year_enter_id` = %s, ' \
                       '`periods_id` = %s, `blocks_id` = %s WHERE `id` = %s'
                cursor.execute(up_t, up_id)
                conn.commit()


class Ui_DeleteQuestion(QtWidgets.QWidget):
    def setupUi(self, DeleteQuestion):
        DeleteQuestion.setObjectName("DeleteQuestion")
        DeleteQuestion.resize(496, 265)
        self.delete_btn = QtWidgets.QPushButton(DeleteQuestion)
        self.delete_btn.setGeometry(QRect(230, 200, 51, 23))
        self.delete_btn.setObjectName("delete_btn")
        self.retranslateUi(DeleteQuestion)
        QtCore.QMetaObject.connectSlotsByName(DeleteQuestion)

    def retranslateUi(self, DeleteQuestion):
        _translate = QCoreApplication.translate
        DeleteQuestion.setWindowTitle(_translate("DeleteQuestion", "Удаление"))
        self.delete_btn.setText(_translate("DeleteQuestion", "Удалить"))


class DeleteQuestion(QtWidgets.QDialog, Ui_DeleteQuestion):
    def __init__(self, data, parent=None):
        sub_name = []
        tea_name = []
        gr_name = []
        cour_name = []
        ye_name = []
        per_name = []
        tt_name = []
        bl_name = []
        sub_name.append(data[0])
        tea_name.append(data[1])
        gr_name.append(data[2])
        cour_name.append(data[3])
        ye_name.append(data[4])
        per_name.append(data[5])
        tt_name.append(data[6])
        bl_name.append(data[7])
        id_data = []
        sel_sub = 'SELECT `id` FROM `subjects` WHERE `name` = %s'
        cursor.execute(sel_sub, sub_name)
        id_data.append(cursor.fetchone()[0])
        sel_tea = 'SELECT `id` FROM `teachers` WHERE `name` = %s'
        cursor.execute(sel_tea, tea_name)
        id_data.append(cursor.fetchone()[0])
        sel_gr = 'SELECT `id` FROM `groups` WHERE `name` = %s'
        cursor.execute(sel_gr, gr_name)
        id_data.append(cursor.fetchone()[0])
        sel_cour = 'SELECT `id` FROM `courses` WHERE `name` = %s'
        cursor.execute(sel_cour, cour_name)
        id_data.append(cursor.fetchone()[0])
        sel_ye = 'SELECT `id` FROM `year_enter` WHERE `name` = %s'
        cursor.execute(sel_ye, ye_name)
        id_data.append(cursor.fetchone()[0])
        sel_per = 'SELECT `id` FROM `periods` WHERE `name` = %s'
        cursor.execute(sel_per, per_name)
        id_data.append(cursor.fetchone()[0])
        sel_tt = 'SELECT `id` FROM `type_tasks` WHERE `name` = %s'
        cursor.execute(sel_tt, tt_name)
        id_data.append(cursor.fetchone()[0])
        sel_bl = 'SELECT `id` FROM `blocks` WHERE `name` = %s'
        cursor.execute(sel_bl, bl_name)
        id_data.append(cursor.fetchone()[0])
        main_id = []
        sel_main_id = 'SELECT `id` FROM `tokens` WHERE `subjects_id` = %s AND `teachers_id` = %s AND `groups_id` = %s AND ' \
                      '`courses_id` = %s AND `year_enter_id` = %s AND `periods_id` = %s AND `type_tasks_id` = %s AND ' \
                      '`blocks_id` = %s'
        cursor.execute(sel_main_id, id_data)
        id_ = cursor.fetchall()
        for i in range(0, len(id_)):
            main_id.append(id_[i][0])
        super(DeleteQuestion, self).__init__(parent)
        self.setupUi(self)
        self.delete_btn.clicked.connect(self.delete_token)
        vopr_id = []
        for i in range(0, len(main_id)):
            id_ = []
            id_.append(main_id[i])
            sel_vopr = 'SELECT * FROM `tokens` WHERE `id` = %s'
            cursor.execute(sel_vopr, id_)
            vopr_id.append(cursor.fetchall()[0])
        self.table = QTableWidget(self)
        self.table.setColumnCount(len(vopr_id[0])+1)
        self.table.setRowCount(len(vopr_id))
        self.table.setHorizontalHeaderLabels(["Статус", "Номер", "Дисциплина", "Задание", "Тип задания", "Преподаватель", "Группа",
                                              "Курсы", "Год поступления", "Период", "Раздел"])
        self.table.horizontalHeaderItem(1).setToolTip("Column 1")
        self.table.horizontalHeaderItem(2).setToolTip("Column 2")
        self.table.horizontalHeaderItem(3).setToolTip("Column 3")
        self.table.horizontalHeaderItem(4).setToolTip("Column 4")
        self.table.horizontalHeaderItem(5).setToolTip("Column 5")
        self.table.horizontalHeaderItem(6).setToolTip("Column 6")
        self.table.horizontalHeaderItem(7).setToolTip("Column 7")
        self.table.horizontalHeaderItem(8).setToolTip("Column 8")
        self.table.horizontalHeaderItem(9).setToolTip("Column 9")
        self.table.horizontalHeaderItem(10).setToolTip("Column 10")
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(4).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(5).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(6).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(7).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(8).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(9).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(10).setTextAlignment(Qt.AlignHCenter)
        for i in range(0, len(vopr_id)):
            v_id = []
            v_id.append(vopr_id[i][0])
            v_id.append(vopr_id[i][1])
            v_id.append(vopr_id[i][2])
            v_id.append(vopr_id[i][3])
            v_id.append(vopr_id[i][4])
            v_id.append(vopr_id[i][5])
            v_id.append(vopr_id[i][6])
            v_id.append(vopr_id[i][7])
            v_id.append(vopr_id[i][8])
            v_id.append(vopr_id[i][9])
            sel_vopr_name = 'SELECT ' \
                            '(SELECT `id` FROM `tokens` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `subjects` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `tasks` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `type_tasks` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `teachers` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `groups` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `courses` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `year_enter` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `periods` WHERE `id` = %s), ' \
                            '(SELECT `name` FROM `blocks` WHERE `id` = %s) ' \
                            'FROM `tokens`'
            cursor.execute(sel_vopr_name, v_id)
            vopr = cursor.fetchone()
            for j in range(0, len(vopr)):
                item = QTableWidgetItem(str(vopr[j]))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table.setItem(i, j+1, item)
            widget = QWidget()
            checkbox = QCheckBox()
            checkbox.setCheckState(Qt.Unchecked)
            layoutH = QHBoxLayout(widget)
            layoutH.addWidget(checkbox)
            layoutH.setAlignment(Qt.AlignCenter)
            layoutH.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(i, 0, widget)
        vlayout = QVBoxLayout(self)
        vlayout.addWidget(self.table)
        vlayout.addWidget(self.delete_btn)

    def delete_token(self):
        checked_list = []
        for i in range(self.table.rowCount()):
            if self.table.cellWidget(i, 0).findChild(type(QCheckBox())).isChecked():
                checked_list.append(self.table.item(i, 1).text())
        for i in range(0, len(checked_list)):
            id_ = []
            id_.append(checked_list[i])
            del_vopr = 'DELETE FROM `tokens` WHERE `id` = %s'
            cursor.execute(del_vopr, id_)
            conn.commit()


class Ui_DeleteTokens(QtWidgets.QWidget):
    def setupUi(self, DeleteTokens):
        DeleteTokens.setObjectName("DeleteTokens")
        DeleteTokens.resize(496, 265)
        self.delete_btn = QtWidgets.QPushButton(DeleteTokens)
        self.delete_btn.setGeometry(QRect(230, 200, 51, 23))
        self.delete_btn.setObjectName("delete_btn")
        self.retranslateUi(DeleteTokens)
        QtCore.QMetaObject.connectSlotsByName(DeleteTokens)

    def retranslateUi(self, DeleteTokens):
        _translate = QCoreApplication.translate
        DeleteTokens.setWindowTitle(_translate("DeleteTokens", "Удаление"))
        self.delete_btn.setText(_translate("DeleteTokens", "Удалить"))


class DeleteTokens(QtWidgets.QDialog, Ui_DeleteTokens):
    def __init__(self, del_data, parent=None):
        super(DeleteTokens, self).__init__(parent)
        self.setupUi(self)
        self.delete_btn.clicked.connect(self.delete_tokens)
        self.table = QTableWidget(self)
        sel_id_data = 'SELECT ' \
                      '(SELECT `id` FROM `subjects` WHERE `name` = %s), ' \
                      '(SELECT `id` FROM `teachers` WHERE `name` = %s), ' \
                      '(SELECT `id` FROM `groups` WHERE `name` = %s), ' \
                      '(SELECT `id` FROM `courses` WHERE `name` = %s), ' \
                      '(SELECT `id` FROM `year_enter` WHERE `name` = %s), ' \
                      '(SELECT `id` FROM `periods` WHERE `name` = %s) ' \
                      'FROM `tokens`'
        cursor.execute(sel_id_data, del_data)
        id_data = cursor.fetchone()
        sel_id_vopr = 'SELECT `id` FROM `tokens` WHERE `subjects_id` = %s AND `teachers_id` = %s AND `groups_id` = %s AND ' \
                      '`courses_id` = %s AND `year_enter_id` = %s AND `periods_id` = %s'
        cursor.execute(sel_id_vopr, id_data)
        id_vopr = cursor.fetchall()
        main_id = []
        for i in range(0, len(id_vopr)):
            id_ = []
            id_.append(id_vopr[i][0])
            sel_date_tokens = 'SELECT `id` FROM `exam_tokens` WHERE `tokens_id` = %s'
            cursor.execute(sel_date_tokens, id_)
            id_tokens = cursor.fetchone()
            if id_tokens != None:
                if id_tokens not in main_id:
                    main_id.append(id_tokens[0])
        right_id = []
        for i in range(0, len(main_id)):
            id_ = []
            id_.append(main_id[i])
            sel_data_tokens = 'SELECT `id`, `number`, `tokens_id`, `date_exam`, `set` FROM `exam_tokens` WHERE `id` = %s'
            cursor.execute(sel_data_tokens, id_)
            right_id.append(cursor.fetchone())
        self.table.setColumnCount(len(right_id[0]) + 1)
        self.table.setRowCount(len(right_id))
        self.table.setHorizontalHeaderLabels(
            ["Статус", "Номер", "Номер билета", "Задание", "Дата экзамена", "Комплект"])
        self.table.horizontalHeaderItem(1).setToolTip("Column 1")
        self.table.horizontalHeaderItem(2).setToolTip("Column 2")
        self.table.horizontalHeaderItem(3).setToolTip("Column 3")
        self.table.horizontalHeaderItem(4).setToolTip("Column 4")
        self.table.horizontalHeaderItem(5).setToolTip("Column 5")
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(4).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(5).setTextAlignment(Qt.AlignHCenter)
        for i in range(0, len(right_id)):
            v_id = []
            v_id.append(right_id[i][0])
            v_id.append(right_id[i][1])
            v_id.append(right_id[i][2])
            v_id.append(right_id[i][3])
            v_id.append(right_id[i][4])
            token_task_id = []
            token_task_id.append(right_id[i][2])
            sel_task_id = 'SELECT `tasks_id` FROM `tokens` WHERE `id` = %s'
            cursor.execute(sel_task_id, token_task_id)
            tasks_id = cursor.fetchone()
            sel_name_tasks = 'SELECT `name` FROM `tasks` WHERE `id` = %s'
            cursor.execute(sel_name_tasks, tasks_id)
            name_tasks = cursor.fetchone()[0]
            for j in range(0, len(v_id)):
                if j == 2:
                    item = QTableWidgetItem(str(name_tasks))
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.table.setItem(i, j + 1, item)
                else:
                    item = QTableWidgetItem(str(v_id[j]))
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.table.setItem(i, j+1, item)
            widget = QWidget()
            checkbox = QCheckBox()
            checkbox.setCheckState(Qt.Unchecked)
            layoutH = QHBoxLayout(widget)
            layoutH.addWidget(checkbox)
            layoutH.setAlignment(Qt.AlignCenter)
            layoutH.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(i, 0, widget)
        vlayout = QVBoxLayout(self)
        vlayout.addWidget(self.table)
        vlayout.addWidget(self.delete_btn)

    def delete_tokens(self):
        checked_list = []
        for i in range(self.table.rowCount()):
            if self.table.cellWidget(i, 0).findChild(type(QCheckBox())).isChecked():
                checked_list.append(self.table.item(i, 1).text())
        for i in range(0, len(checked_list)):
            id_ = []
            id_.append(checked_list[i])
            del_token = 'DELETE FROM `exam_tokens` WHERE `id` = %s'
            cursor.execute(del_token, id_)
            conn.commit()


class Ui_OptionsDB(QtWidgets.QWidget):
    def setupUi(self, OptionsDB):
        OptionsDB.setObjectName("OptionsDB")
        OptionsDB.resize(496, 265)
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
        self.name_line.setText(_translate("OptionsDB", "Логин:"))
        self.pass_line.setText(_translate("OptionsDB", "Пароль:"))
        self.host_line.setText(_translate("OptionsDB", "Хост:"))
        self.db_line.setText(_translate("OptionsDB", "База данных:"))
        self.save_btn.setText(_translate("OptionsDB", "Сохранить"))


class OptionsDB(QtWidgets.QDialog, Ui_OptionsDB):
    def __init__(self, parent=None):
        super(OptionsDB, self).__init__(parent)
        self.setupUi(self)
        vl = QVBoxLayout(self)
        vl.addWidget(self.name_line)
        vl.addWidget(self.pass_line)
        vl.addWidget(self.host_line)
        vl.addWidget(self.db_line)
        vl.addWidget(self.save_btn)
        self.save_btn.clicked.connect(self.save_)

    def save_(self):
        data = {'login': self.name_line.text(), 'password': self.pass_line.text(), 'host': self.host_line.text(), 'name_db': self.db_line.text()}
        with open('config_db.json', 'w') as save:
            json.dump(data, save)


class Ui_ViewUsers(QtWidgets.QWidget):
    def setupUi(self, ViewUsers):
        ViewUsers.setObjectName("ViewUsers")
        ViewUsers.resize(496, 265)
        self.retranslateUi(ViewUsers)
        QtCore.QMetaObject.connectSlotsByName(ViewUsers)

    def retranslateUi(self, ViewUsers):
        _translate = QCoreApplication.translate
        ViewUsers.setWindowTitle(_translate("ViewUsers", "Список пользователей"))


class ViewUsers(QtWidgets.QDialog, Ui_ViewUsers):
    def __init__(self, parent=None):
        super(ViewUsers, self).__init__(parent)
        self.setupUi(self)
        cursor.execute('SELECT * FROM `users`')
        id_uch = cursor.fetchall()
        self.table = QTableWidget(self)
        self.table.setColumnCount(len(id_uch[0]))
        self.table.setRowCount(len(id_uch))
        self.table.setHorizontalHeaderLabels(
            ["Номер", "Логин", "Пароль", "Роль", "Преподаватель"])
        for i in range(0, len(id_uch)):
            id_ = []
            id_.append(id_uch[i][0])
            id_.append(id_uch[i][0])
            id_.append(id_uch[i][0])
            id_.append(id_uch[i][3])
            id_.append(id_uch[i][4])
            sel_profile = 'SELECT ' \
                          '(SELECT `id` FROM `users` WHERE `id` = %s), ' \
                          '(SELECT `login` FROM `users` WHERE `id` = %s), ' \
                          '(SELECT `password` FROM `users` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `roles` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `teachers` WHERE `id` = %s) ' \
                          'FROM `users`'
            cursor.execute(sel_profile, id_)
            profile = cursor.fetchone()
            for j in range(0, len(profile)):
                item = QTableWidgetItem(str(profile[j]))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table.setItem(i, j, item)


class Ui_UpdateUsers(QtWidgets.QWidget):
    def setupUi(self, UpdateUsers):
        UpdateUsers.setObjectName("UpdateUsers")
        UpdateUsers.resize(496, 265)
        self.update_btn = QtWidgets.QPushButton(UpdateUsers)
        self.update_btn.setGeometry(QRect(230, 200, 51, 23))
        self.update_btn.setObjectName("update_btn")
        self.retranslateUi(UpdateUsers)
        QtCore.QMetaObject.connectSlotsByName(UpdateUsers)

    def retranslateUi(self, UpdateUsers):
        _translate = QCoreApplication.translate
        UpdateUsers.setWindowTitle(_translate("UpdateUsers", "Редактирование пользователей"))
        self.update_btn.setText(_translate("UpdateUsers", "Редактировать"))


class UpdateUsers(QtWidgets.QDialog, Ui_UpdateUsers):
    def __init__(self, parent=None):
        super(UpdateUsers, self).__init__(parent)
        self.setupUi(self)
        self.update_btn.clicked.connect(self.update_users)
        cursor.execute('SELECT `id`, `roles_id`, `teachers_id` FROM `users`')
        id_uch = cursor.fetchall()
        self.table = QTableWidget(self)
        self.table.setColumnCount(len(id_uch[0]))
        self.table.setRowCount(len(id_uch))
        self.table.setHorizontalHeaderLabels(
            ["Номер", "Логин", "Пароль", "Роль", "Преподаватель"])
        for i in range(0, len(id_uch)):
            id_ = []
            id_.append(id_uch[i][0])
            id_.append(id_uch[i][0])
            id_.append(id_uch[i][0])
            id_.append(id_uch[i][1])
            id_.append(id_uch[i][2])
            sel_profile = 'SELECT ' \
                          '(SELECT `id` FROM `users` WHERE `id` = %s), ' \
                          '(SELECT `login` FROM `users` WHERE `id` = %s), ' \
                          '(SELECT `password` FROM `users` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `roles` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `teachers` WHERE `id` = %s) ' \
                          'FROM `users`'
            cursor.execute(sel_profile, id_)
            profile = cursor.fetchone()
            for j in range(0, len(profile)):
                if j == 0:
                    item = QTableWidgetItem(str(profile[j]))
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.table.setItem(i, j, item)
                else:
                    self.table.setItem(i, j, QTableWidgetItem(str(profile[j])))
        vl = QVBoxLayout(self)
        vl.addWidget(self.table)
        vl.addWidget(self.update_btn)

    def update_users(self):
        for i in range(self.table.rowCount()):
            tb_data = []
            for j in range(0, self.table.columnCount()):
                tb_data.append(self.table.item(i, j).text())
            login_name = []
            login_name.append(tb_data[i][1])
            sel_count_login = 'SELECT `id`, `login` FROM `users` WHERE `login` = %s'
            cursor.execute(sel_count_login, login_name)
            check_login = cursor.fetchall()
            if check_login != None:
                if check_login[0][0] != tb_data[i][0]:
                    self.dlg = QMessageBox()
                    self.dlg.addButton("Ок", QMessageBox.AcceptRole)
                    self.dlg.setIcon(QMessageBox.Warning)
                    self.dlg.setWindowTitle("Ошибка!")
                    self.dlg.setInformativeText(
                        "Пользователь с логином " + str(tb_data[i][1]) + " уже существует!")
                    bttn = self.dlg.exec()
                    if self.dlg.clickedButton().text() == "Ок":
                        continue
            role_name = []
            role_name.append(tb_data[i][3])
            sel_id_role = 'SELECT `id` FROM `roles` WHERE `name` = %s'
            cursor.execute(sel_id_role, role_name)
            if cursor.fetchone() != None:
                if role_name != 'Преподаватель':
                    tb_data[i][4] = None
                else:
                    tea_name = []
                    tea_name.append(tb_data[i][4])
                    sel_id_tea = 'SELECT `id` FROM `teachers` FROM `name` = %s'
                    cursor.execute(sel_id_tea, tea_name)
                    if cursor.fetchone() != None:
                        self.dlg = QMessageBox()
                        self.dlg.addButton("Ок", QMessageBox.AcceptRole)
                        self.dlg.setIcon(QMessageBox.Warning)
                        self.dlg.setWindowTitle("Ошибка!")
                        self.dlg.setInformativeText(
                            "Указанный преподаватель " + str(tb_data[i][4]) + " не найден в системе!")
                        bttn = self.dlg.exec()
                        if self.dlg.clickedButton().text() == "Ок":
                            continue
            else:
                self.dlg = QMessageBox()
                self.dlg.addButton("Ок", QMessageBox.AcceptRole)
                self.dlg.setIcon(QMessageBox.Warning)
                self.dlg.setWindowTitle("Ошибка!")
                self.dlg.setInformativeText(
                    "Роли " + str(tb_data[i][3]) + " не существует!")
                bttn = self.dlg.exec()
                if self.dlg.clickedButton().text() == "Ок":
                    continue
            sel_user = 'SELECT ' \
                       '(SELECT `id` FROM `users` WHERE `id` = %s), ' \
                       '(SELECT `login` FROM `users` WHERE `login` = %s), ' \
                       '(SELECT `password` FROM `users` WHERE `password` = %s), ' \
                       '(SELECT `id` FROM `roles` WHERE `name` = %s), ' \
                       '(SELECT `id` FROM `teachers` WHERE `name` = %s) ' \
                       'FROM `users`'
            cursor.execute(sel_user, tb_data)
            if cursor.fetchone() == None:
                sel_id_role = 'SELECT `id` FROM `roles` WHERE `name` = %s'
                cursor.execute(sel_id_role, role_name)
                tb_data[i][3] = cursor.fetchone()[0]
                if role_name != 'Преподаватель':
                    tb_data[i][4] = None
                else:
                    tea_name = []
                    tea_name.append(tb_data[i][4])
                    sel_id_tea = 'SELECT `id` FROM `teachers` FROM `name` = %s'
                    cursor.execute(sel_id_tea, tea_name)
                    tb_data[i][4] = cursor.fetchone()[0]
                update_data = []
                update_data.append(tb_data[i][1])
                update_data.append(tb_data[i][2])
                update_data.append(tb_data[i][3])
                update_data.append(tb_data[i][4])
                update_data.append(tb_data[i][0])
                update_user = 'UPDATE `users` SET `login` = %s, `password` = %s, `roles_id` = %s, `teachers_id` = %s ' \
                              'WHERE `id` = %s'
                cursor.execute(update_user, update_data)
                conn.commit()


class Ui_DeleteUsers(QtWidgets.QWidget):
    def setupUi(self, DeleteUsers):
        DeleteUsers.setObjectName("DeleteUsers")
        DeleteUsers.resize(496, 265)
        self.delete_btn = QtWidgets.QPushButton(DeleteUsers)
        self.delete_btn.setGeometry(QRect(230, 200, 51, 23))
        self.delete_btn.setObjectName("delete_btn")
        self.retranslateUi(DeleteUsers)
        QtCore.QMetaObject.connectSlotsByName(DeleteUsers)

    def retranslateUi(self, DeleteUsers):
        _translate = QCoreApplication.translate
        DeleteUsers.setWindowTitle(_translate("DeleteUsers", "Удаление пользователей"))
        self.delete_btn.setText(_translate("DeleteUsers", "Удалить"))


class DeleteUsers(QtWidgets.QDialog, Ui_DeleteUsers):
    def __init__(self, parent=None):
        super(DeleteUsers, self).__init__(parent)
        self.setupUi(self)
        self.delete_btn.clicked.connect(self.delete_users)
        cursor.execute('SELECT * FROM `users`')
        id_uch = cursor.fetchall()
        self.table = QTableWidget(self)
        self.table.setColumnCount(len(id_uch[0])+1)
        self.table.setRowCount(len(id_uch))
        self.table.setHorizontalHeaderLabels(
            ["Статус", "Номер", "Логин", "Пароль", "Роль", "Преподаватель"])
        for i in range(0, len(id_uch)):
            id_ = []
            id_.append(id_uch[i][0])
            id_.append(id_uch[i][0])
            id_.append(id_uch[i][0])
            id_.append(id_uch[i][3])
            id_.append(id_uch[i][4])
            sel_profile = 'SELECT ' \
                          '(SELECT `id` FROM `users` WHERE `id` = %s), ' \
                          '(SELECT `login` FROM `users` WHERE `id` = %s), ' \
                          '(SELECT `password` FROM `users` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `roles` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `teachers` WHERE `id` = %s) ' \
                          'FROM `users`'
            cursor.execute(sel_profile, id_)
            profile = cursor.fetchone()
            for j in range(0, len(profile)):
                item = QTableWidgetItem(str(profile[j]))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table.setItem(i, j+1, item)
            widget = QWidget()
            checkbox = QCheckBox()
            checkbox.setCheckState(Qt.Unchecked)
            layoutH = QHBoxLayout(widget)
            layoutH.addWidget(checkbox)
            layoutH.setAlignment(Qt.AlignCenter)
            layoutH.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(i, 0, widget)
        vl = QVBoxLayout(self)
        vl.addWidget(self.table)
        vl.addWidget(self.delete_btn)

    def delete_users(self):
        checked_list = []
        for i in range(self.table.rowCount()):
            if self.table.cellWidget(i, 0).findChild(type(QCheckBox())).isChecked():
                checked_list.append(self.table.item(i, 1).text())
        for i in range(0, len(checked_list)):
            id_ = []
            id_.append(checked_list[i])
            del_vopr = 'DELETE FROM `users` WHERE `id` = %s'
            cursor.execute(del_vopr, id_)
            conn.commit()


class Ui_OptionsUsers(QtWidgets.QWidget):
    def setupUi(self, OptionsUsers):
        OptionsUsers.setObjectName("OptionsUsers")
        OptionsUsers.resize(496, 265)
        self.add_user_btn = QtWidgets.QPushButton(OptionsUsers)
        self.add_user_btn.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.add_user_btn.setObjectName("add_user_btn")
        self.view_user_btn = QtWidgets.QPushButton(OptionsUsers)
        self.view_user_btn.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.view_user_btn.setObjectName("view_user_btn")
        self.update_user_btn = QtWidgets.QPushButton(OptionsUsers)
        self.update_user_btn.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.update_user_btn.setObjectName("update_user_btn")
        self.delete_user_btn = QtWidgets.QPushButton(OptionsUsers)
        self.delete_user_btn.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.delete_user_btn.setObjectName("delete_user_btn")
        self.retranslateUi(OptionsUsers)
        QtCore.QMetaObject.connectSlotsByName(OptionsUsers)

    def retranslateUi(self, OptionsUsers):
        _translate = QCoreApplication.translate
        OptionsUsers.setWindowTitle(_translate("OptionsUsers", "Конфигурация пользователей"))
        self.add_user_btn.setText(_translate("OptionsUsers", "Создать новую учётную запись"))
        self.view_user_btn.setText(_translate("OptionsUsers", "Открыть список пользователей"))
        self.update_user_btn.setText(_translate("OptionsUsers", "Редактирование пользователей"))
        self.delete_user_btn.setText(_translate("OptionsUsers", "Удаление пользователей"))


class OptionsUsers(QtWidgets.QDialog, Ui_OptionsUsers):
    def __init__(self, parent=None):
        super(OptionsUsers, self).__init__(parent)
        self.setupUi(self)
        vl = QVBoxLayout(self)
        vl.addWidget(self.add_user_btn)
        vl.addWidget(self.view_user_btn)
        vl.addWidget(self.update_user_btn)
        vl.addWidget(self.delete_user_btn)
        self.add_user_btn.clicked.connect(self.add_user)
        self.view_user_btn.clicked.connect(self.view_user)
        self.update_user_btn.clicked.connect(self.update_user)
        self.delete_user_btn.clicked.connect(self.delete_user)

    def add_user(self):
        self.AU = Dialog(self)
        self.AU.show()

    def view_user(self):
        self.VU = ViewUsers(self)
        self.VU.show()

    def update_user(self):
        self.UU = UpdateUsers(self)
        self.UU.show()

    def delete_user(self):
        self.DU = DeleteUsers(self)
        self.DU.show()


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
        self.textBox = QPlainTextEdit(self.widget)
        self.textBox.move(250, 120)
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
        self.output_v = QtWidgets.QPushButton(self.centralwidget)
        self.output_v.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.output_v.setObjectName("output_v")
        self.output_v.findChild(QPushButton, 'output_v')
        self.next_ = QtWidgets.QPushButton(self.centralwidget)
        self.next_.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.next_.setObjectName("next_")
        self.next_.findChild(QPushButton, 'next_')
        self.gen_b = QtWidgets.QPushButton(self.centralwidget)
        self.gen_b.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.gen_b.setObjectName("gen_b")
        self.gen_b.findChild(QPushButton, 'gen_b')
        self.options_db = QtWidgets.QPushButton(self.centralwidget)
        self.options_db.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.options_db.setObjectName("options_db")
        self.options_db.findChild(QPushButton, 'options_db')
        self.options_users = QtWidgets.QPushButton(self.centralwidget)
        self.options_users.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.options_users.setObjectName("options_users")
        self.options_users.findChild(QPushButton, 'options_users')
        self.add_t = QtWidgets.QPushButton(self.centralwidget)
        self.add_t.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.add_t.setObjectName("add_t")
        self.add_t.findChild(QPushButton, 'add_t')
        self.update_t = QtWidgets.QPushButton(self.centralwidget)
        self.update_t.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.update_t.setObjectName("update_t")
        self.update_t.findChild(QPushButton, 'update_t')
        self.delete_t = QtWidgets.QPushButton(self.centralwidget)
        self.delete_t.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.delete_t.setObjectName("delete_t")
        self.delete_t.findChild(QPushButton, 'delete_t')
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
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        self.label_21.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_21.setObjectName("label_21")
        self.label_23 = QtWidgets.QLabel(self.centralwidget)
        self.label_23.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.centralwidget)
        self.label_24.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_24.setObjectName("label_24")
        self.label_25 = QtWidgets.QLabel(self.centralwidget)
        self.label_25.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(self.centralwidget)
        self.label_26.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(self.centralwidget)
        self.label_27.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_27.setObjectName("label_27")
        self.label_28 = QtWidgets.QLabel(self.centralwidget)
        self.label_28.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_28.setObjectName("label_28")
        self.label_29 = QtWidgets.QLabel(self.centralwidget)
        self.label_29.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_29.setObjectName("label_29")
        self.label_31 = QtWidgets.QLabel(self.centralwidget)
        self.label_31.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_31.setObjectName("label_31")
        self.label_32 = QtWidgets.QLabel(self.centralwidget)
        self.label_32.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_32.setObjectName("label_32")
        self.label_33 = QtWidgets.QLabel(self.centralwidget)
        self.label_33.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_33.setObjectName("label_33")
        self.label_34 = QtWidgets.QLabel(self.centralwidget)
        self.label_34.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_34.setObjectName("label_34")
        self.label_35 = QtWidgets.QLabel(self.centralwidget)
        self.label_35.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_35.setObjectName("label_35")
        self.label_36 = QtWidgets.QLabel(self.centralwidget)
        self.label_36.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_36.setObjectName("label_36")
        self.label_37 = QtWidgets.QLabel(self.centralwidget)
        self.label_37.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_37.setObjectName("label_37")
        self.label_38 = QtWidgets.QLabel(self.centralwidget)
        self.label_38.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_38.setObjectName("label_38")
        self.label_41 = QtWidgets.QLabel(self.centralwidget)
        self.label_41.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_41.setObjectName("label_41")
        self.label_42 = QtWidgets.QLabel(self.centralwidget)
        self.label_42.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_42.setObjectName("label_42")
        self.label_43 = QtWidgets.QLabel(self.centralwidget)
        self.label_43.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_43.setObjectName("label_43")
        self.label_44 = QtWidgets.QLabel(self.centralwidget)
        self.label_44.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_44.setObjectName("label_44")
        self.label_45 = QtWidgets.QLabel(self.centralwidget)
        self.label_45.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_45.setObjectName("label_45")
        self.label_46 = QtWidgets.QLabel(self.centralwidget)
        self.label_46.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_46.setObjectName("label_46")
        self.label_47 = QtWidgets.QLabel(self.centralwidget)
        self.label_47.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_47.setObjectName("label_47")
        self.label_48 = QtWidgets.QLabel(self.centralwidget)
        self.label_48.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_48.setObjectName("label_48")
        self.label_51 = QtWidgets.QLabel(self.centralwidget)
        self.label_51.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_51.setObjectName("label_51")
        self.label_52 = QtWidgets.QLabel(self.centralwidget)
        self.label_52.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_52.setObjectName("label_52")
        self.label_53 = QtWidgets.QLabel(self.centralwidget)
        self.label_53.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_53.setObjectName("label_53")
        self.label_54 = QtWidgets.QLabel(self.centralwidget)
        self.label_54.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_54.setObjectName("label_54")
        self.label_55 = QtWidgets.QLabel(self.centralwidget)
        self.label_55.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_55.setObjectName("label_55")
        self.label_56 = QtWidgets.QLabel(self.centralwidget)
        self.label_56.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_56.setObjectName("label_56")
        self.blocks_line = QtWidgets.QLineEdit(self.centralwidget)
        self.blocks_line.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.blocks_line.setObjectName("blocks_line")
        self.tokens_line = QtWidgets.QLineEdit(self.centralwidget)
        self.tokens_line.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.tokens_line.setObjectName("tokens_line")
        self.tasks_line = QtWidgets.QLineEdit(self.centralwidget)
        self.tasks_line.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.tasks_line.setObjectName("tasks_line")
        self.uch_org_line = QtWidgets.QLineEdit(self.centralwidget)
        self.uch_org_line.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.uch_org_line.setObjectName("uch_org_line")
        self.full_name_line = QtWidgets.QLineEdit(self.centralwidget)
        self.full_name_line.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.full_name_line.setObjectName("full_name_line")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 241, 17))
        self.label_2.setObjectName("label_2")
        self.filename_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.filename_2.setGeometry(QtCore.QRect(10, 130, 221, 25))
        self.filename_2.setObjectName("filename_2")
        self.delete_token = QtWidgets.QPushButton(self.centralwidget)
        self.delete_token.setGeometry(QtCore.QRect(30, 150, 241, 55))
        self.delete_token.setObjectName("delete_token")
        self.delete_token.findChild(QPushButton, 'delete_token')
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
        self.label_56.setText(_translate("MainWindow", "Выберите период:"))
        self.label_55.setText(_translate("MainWindow", "Выберите год поступления:"))
        self.label_54.setText(_translate("MainWindow", "Выберите курс:"))
        self.label_53.setText(_translate("MainWindow", "Выберите группу:"))
        self.label_52.setText(_translate("MainWindow", "Выберите преподавателя:"))
        self.label_51.setText(_translate("MainWindow", "Выберите дисциплину:"))
        self.label_48.setText(_translate("MainWindow", "Выберите модуль/раздел:"))
        self.label_47.setText(_translate("MainWindow", "Выберите тип задания:"))
        self.label_46.setText(_translate("MainWindow", "Выберите период:"))
        self.label_45.setText(_translate("MainWindow", "Выберите год поступления:"))
        self.label_44.setText(_translate("MainWindow", "Выберите курс:"))
        self.label_43.setText(_translate("MainWindow", "Выберите группу:"))
        self.label_42.setText(_translate("MainWindow", "Выберите преподавателя:"))
        self.label_41.setText(_translate("MainWindow", "Выберите дисциплину:"))
        self.label_38.setText(_translate("MainWindow", "Выберите модуль/раздел:"))
        self.label_37.setText(_translate("MainWindow", "Выберите тип задания:"))
        self.label_36.setText(_translate("MainWindow", "Выберите период:"))
        self.label_35.setText(_translate("MainWindow", "Выберите год поступления:"))
        self.label_34.setText(_translate("MainWindow", "Выберите курс:"))
        self.label_33.setText(_translate("MainWindow", "Выберите группу:"))
        self.label_32.setText(_translate("MainWindow", "Выберите преподавателя:"))
        self.label_31.setText(_translate("MainWindow", "Выберите дисциплину:"))
        self.label_29.setText(_translate("MainWindow", "Введите название модуля/раздела:"))
        self.label_28.setText(_translate("MainWindow", "Выберите тип задания:"))
        self.label_27.setText(_translate("MainWindow", "Выберите период:"))
        self.label_26.setText(_translate("MainWindow", "Выберите год поступления:"))
        self.label_25.setText(_translate("MainWindow", "Выберите курс:"))
        self.label_24.setText(_translate("MainWindow", "Выберите группу:"))
        self.label_23.setText(_translate("MainWindow", "Выберите преподавателя:"))
        self.label_21.setText(_translate("MainWindow", "Выберите дисциплину:"))
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
        self.delete_token.setText(_translate("MainWindow", "Просмотреть"))
        self.options_db.setText(_translate("MainWindow", "Настроить базу данных"))
        self.options_users.setText(_translate("MainWindow", "Настроить пользователей"))
        self.delete_t.setText(_translate("MainWindow", "Просмотреть"))
        self.update_t.setText(_translate("MainWindow", "Просмотреть"))
        self.add_t.setText(_translate("MainWindow", "Сохранить"))
        self.next_.setText(_translate("MainWindow", "Продолжить"))
        self.output_token.setText(_translate("MainWindow", "Билет"))
        self.gen_b.setText(_translate("MainWindow", "Сгенерировать билет"))
        self.open_pars.setText(_translate("MainWindow", "Обзор..."))
        self.pars_.setText(_translate("MainWindow", "Загрузить"))
        self.output_.setText(_translate("MainWindow", "Выгрузить билеты"))
        self.output_v.setText(_translate("MainWindow", "Выгрузить вопросы"))
        # текствые поля (lineEdit)
        self.tasks_line.setText(_translate("MainWindow", "Количество заданий"))
        self.tokens_line.setText(_translate("MainWindow", "Количество билетов"))
        self.uch_org_line.setText(_translate("MainWindow", "Название организации"))
        self.full_name_line.setText(_translate("MainWindow", "Полное название дисциплины"))
        # чекбоксы (checkBox)
        self.checkBox_practic_gen.setText(_translate("MainWindow", "Добавить практические задания"))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    # глобальные переменные
    file_ = ''
    practic = False

    # основаная логика приложения
    def __init__(self, login):
        sel_test = 'SELECT * FROM `users` WHERE `login` = %s'
        l = []
        l.append(login)
        cursor.execute(sel_test, l)
        self.user = cursor.fetchone()
        super().__init__()
        self.setupUi(self)
        self.parser = QWidget()
        self.generator_ = QWidget()
        self.output = QWidget()
        self.create_question_ = QWidget()
        self.update_question_ = QWidget()
        self.delete_question_ = QWidget()
        self.admin_ = QWidget()
        self.delete_tokens_ = QWidget()
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.addTab(self.parser, "Загрузка")
        self.tabWidget.addTab(self.generator_, "Генератор")
        self.tabWidget.addTab(self.output, "Выгрузка")
        self.tabWidget.addTab(self.create_question_, "Добавление вопросов")
        self.tabWidget.addTab(self.update_question_, "Обновление вопросов")
        self.tabWidget.addTab(self.delete_question_, "Удаление вопросов")
        self.tabWidget.addTab(self.admin_, "Администрирование")
        self.tabWidget.addTab(self.delete_tokens_, "Удаление билетов")
        self.parserUI()
        self.generatorUI()
        self.outputUI()
        self.create_question_Ui()
        self.update_question_Ui()
        self.delete_question_Ui()
        self.adminIs_Ui()
        self.delete_tokens_Ui()
        self.delete_token.clicked.connect(self.delete_tokens)
        self.delete_t.clicked.connect(self.delete_question)
        self.update_t.clicked.connect(self.update_question)
        self.add_t.clicked.connect(self.create_question)
        self.gen_b.clicked.connect(self.NumTasksUI)
        self.next_.clicked.connect(self.generator)
        self.open_pars.clicked.connect(self.pars_win)
        self.pars_.clicked.connect(self.pars)
        self.output_.clicked.connect(self.gen_out)
        self.output_v.clicked.connect(self.output_vopr)
        self.options_db.clicked.connect(self.optionsDB)
        self.options_users.clicked.connect(self.optionsUsers)
        self.checkBox_practic_gen.stateChanged.connect(self.clickBox)
        self.showFullScreen()

    # окно добавления вопросов
    def create_question_Ui(self):
        if self.user[4] != None:
            teacher = []
            teacher.append(self.user[4])
            sel_sub = 'SELECT DISTINCT `subjects_id` ' \
                     'FROM `tokens` WHERE `teachers_id` = %s'
            sel_tea = 'SELECT DISTINCT `teachers_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_gr = 'SELECT DISTINCT `groups_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_cour = 'SELECT DISTINCT `courses_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_ye = 'SELECT DISTINCT `year_enter_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_per = 'SELECT DISTINCT `periods_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            cursor.execute(sel_sub, teacher)
            sub = cursor.fetchall()
            cursor.execute(sel_tea, teacher)
            tea = cursor.fetchall()
            cursor.execute(sel_gr, teacher)
            gr = cursor.fetchall()
            cursor.execute(sel_cour, teacher)
            cour = cursor.fetchall()
            cursor.execute(sel_ye, teacher)
            ye = cursor.fetchall()
            cursor.execute(sel_per, teacher)
            per = cursor.fetchall()
            self.combo30 = QComboBox(self)
            for i in range(0, len(sub)):
                sub_id = []
                sub_id.append(int(sub[i][0]))
                sel_sub_name = 'SELECT `name` FROM `subjects` WHERE `id` = %s'
                cursor.execute(sel_sub_name, sub_id)
                self.combo30.addItem(cursor.fetchone()[0])
            self.combo31 = QComboBox(self)
            for i in range(0, len(tea)):
                tea_id = []
                tea_id.append(int(tea[i][0]))
                sel_tea_name = 'SELECT `name` FROM `teachers` WHERE `id` = %s'
                cursor.execute(sel_tea_name, tea_id)
                self.combo31.addItem(cursor.fetchone()[0])
            self.combo32 = QComboBox(self)
            for i in range(0, len(gr)):
                gr_id = []
                gr_id.append(int(gr[i][0]))
                sel_gr_name = 'SELECT `name` FROM `groups` WHERE `id` = %s'
                cursor.execute(sel_gr_name, gr_id)
                self.combo32.addItem(cursor.fetchone()[0])
            self.combo33 = QComboBox(self)
            for i in range(0, len(cour)):
                cour_id = []
                cour_id.append(int(cour[i][0]))
                sel_cour_name = 'SELECT `name` FROM `courses` WHERE `id` = %s'
                cursor.execute(sel_cour_name, cour_id)
                self.combo33.addItem(cursor.fetchone()[0])
            self.combo34 = QComboBox(self)
            for i in range(0, len(ye)):
                ye_id = []
                ye_id.append(int(ye[i][0]))
                sel_ye_name = 'SELECT `name` FROM `year_enter` WHERE `id` = %s'
                cursor.execute(sel_ye_name, ye_id)
                self.combo34.addItem(cursor.fetchone()[0])
            self.combo35 = QComboBox(self)
            for i in range(0, len(per)):
                per_id = []
                per_id.append(int(per[i][0]))
                sel_per_name = 'SELECT `name` FROM `periods` WHERE `id` = %s'
                cursor.execute(sel_per_name, per_id)
                self.combo35.addItem(cursor.fetchone()[0])
            self.combo36 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `type_tasks`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo36.addItem(check_sel[i][0])
        else:
            self.combo30 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `subjects`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo30.addItem(check_sel[i][0])
            self.combo31 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `teachers`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo31.addItem(check_sel[i][0])
            self.combo32 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `groups`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo32.addItem(check_sel[i][0])
            self.combo33 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `courses`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo33.addItem(check_sel[i][0])
            self.combo34 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `year_enter`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo34.addItem(check_sel[i][0])
            self.combo35 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `periods`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo35.addItem(check_sel[i][0])
            self.combo36 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `type_tasks`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo36.addItem(check_sel[i][0])
        hlayout = QHBoxLayout(self)
        self.tabWidget = QTabWidget(self.centralwidget)
        hlayout.addWidget(self.label_21)
        vlayout = QVBoxLayout(self)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.combo30)
        vlayout1 = QVBoxLayout(self)
        vlayout1.addLayout(vlayout)
        vlayout1.addWidget(self.label_23)
        vlayout2 = QVBoxLayout(self)
        vlayout2.addLayout(vlayout1)
        vlayout2.addWidget(self.combo31)
        vlayout3 = QVBoxLayout(self)
        vlayout3.addLayout(vlayout2)
        vlayout3.addWidget(self.label_24)
        vlayout4 = QVBoxLayout(self)
        vlayout4.addLayout(vlayout3)
        vlayout4.addWidget(self.combo32)
        vlayout5 = QVBoxLayout(self)
        vlayout5.addLayout(vlayout4)
        vlayout5.addWidget(self.label_25)
        vlayout6 = QVBoxLayout(self)
        vlayout6.addLayout(vlayout5)
        vlayout6.addWidget(self.combo33)
        vlayout7 = QVBoxLayout(self)
        vlayout7.addLayout(vlayout6)
        vlayout7.addWidget(self.label_26)
        vlayout8 = QVBoxLayout(self)
        vlayout8.addLayout(vlayout7)
        vlayout8.addWidget(self.combo34)
        vlayout9 = QVBoxLayout(self)
        vlayout9.addLayout(vlayout8)
        vlayout9.addWidget(self.label_27)
        vlayout10 = QVBoxLayout(self)
        vlayout10.addLayout(vlayout9)
        vlayout10.addWidget(self.combo35)
        vlayout11 = QVBoxLayout(self)
        vlayout11.addLayout(vlayout10)
        vlayout11.addWidget(self.label_28)
        vlayout12 = QVBoxLayout(self)
        vlayout12.addLayout(vlayout11)
        vlayout12.addWidget(self.combo36)
        vlayout13 = QVBoxLayout(self)
        vlayout13.addLayout(vlayout12)
        vlayout13.addWidget(self.label_29)
        vlayout14 = QVBoxLayout(self)
        vlayout14.addLayout(vlayout13)
        vlayout14.addWidget(self.blocks_line)
        hlayout1 = QHBoxLayout(self)
        hlayout1.addLayout(vlayout14)
        hlayout1.addWidget(self.textBox)
        vlayout15 = QVBoxLayout(self)
        vlayout15.addLayout(hlayout1)
        vlayout15.addWidget(self.add_t)
        self.tabWidget.setTabText(3, "CteateQ")
        self.create_question_.setLayout(vlayout15)

    # добавление вопросов
    def create_question(self):
        data = []
        data.append(self.combo30.currentText())
        data.append(self.combo31.currentText())
        data.append(self.combo32.currentText())
        data.append(self.combo33.currentText())
        data.append(self.combo34.currentText())
        data.append(self.combo35.currentText())
        data.append(self.combo36.currentText())
        data.append(self.blocks_line.text())
        data.append(self.textBox.toPlainText())
        data_id = []
        name_sub = []
        name_tea = []
        name_gr = []
        name_cour = []
        name_ye = []
        name_per = []
        name_tt = []
        name_bl = []
        name_tas = []
        name_sub.append(data[0])
        name_tea.append(data[1])
        name_gr.append(data[2])
        name_cour.append(data[3])
        name_ye.append(data[4])
        name_per.append(data[5])
        name_tt.append(data[6])
        name_bl.append(data[7])
        name_tas.append(data[8])
        sel_sub = 'SELECT `id` FROM `subjects` WHERE `name` = %s'
        sel_tea = 'SELECT `id` FROM `teachers` WHERE `name` = %s'
        sel_gr = 'SELECT `id` FROM `groups` WHERE `name` = %s'
        sel_cour = 'SELECT `id` FROM `courses` WHERE `name` = %s'
        sel_ye = 'SELECT `id` FROM `year_enter` WHERE `name` = %s'
        sel_per = 'SELECT `id` FROM `periods` WHERE `name` = %s'
        sel_tt = 'SELECT `id` FROM `type_tasks` WHERE `name` = %s'
        cursor.execute(sel_sub, name_sub)
        data_id.append(cursor.fetchone()[0])
        cursor.execute(sel_tea, name_tea)
        data_id.append(cursor.fetchone()[0])
        cursor.execute(sel_gr, name_gr)
        data_id.append(cursor.fetchone()[0])
        cursor.execute(sel_cour, name_cour)
        data_id.append(cursor.fetchone()[0])
        cursor.execute(sel_ye, name_ye)
        data_id.append(cursor.fetchone()[0])
        cursor.execute(sel_per, name_per)
        data_id.append(cursor.fetchone()[0])
        cursor.execute(sel_tt, name_tt)
        data_id.append(cursor.fetchone()[0])
        in_block = 'INSERT INTO `blocks` (`name`) VALUES (%s)'
        check_in = 'SELECT * FROM `blocks` WHERE `name` = %s'
        cursor.execute(check_in, name_bl)
        check_ = cursor.fetchone()
        if check_ == None:
            cursor.execute(in_block, name_bl)
        sel_id_block = 'SELECT `id` FROM `blocks` WHERE `name` = %s'
        cursor.execute(sel_id_block, name_bl)
        data_id.append(cursor.fetchone()[0])
        in_task = 'INSERT INTO `tasks` (`name`) VALUES (%s)'
        check_in = 'SELECT * FROM `tasks` WHERE `name` = %s'
        cursor.execute(check_in, name_tas)
        check_ = cursor.fetchone()
        if check_ == None:
            cursor.execute(in_task, name_tas)
        sel_id_task = 'SELECT `id` FROM `tasks` WHERE `name` = %s'
        cursor.execute(sel_id_task, name_tas)
        data_id.append(cursor.fetchone()[0])
        in_token = 'INSERT INTO `tokens` (`subjects_id`, `teachers_id`, `groups_id`, `courses_id`, `year_enter_id`, ' \
                   '`periods_id`, `type_tasks_id`, `blocks_id`, `tasks_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        check_in = 'SELECT * FROM `tokens` WHERE `subjects_id` = %s AND `teachers_id` = %s AND `groups_id` = %s AND ' \
                   '`courses_id` = %s AND `year_enter_id` = %s AND `periods_id` = %s AND `type_tasks_id` = %s AND ' \
                   '`blocks_id` = %s AND `tasks_id` = %s'
        cursor.execute(check_in, data_id)
        if cursor.fetchone() == None:
            cursor.execute(in_token, data_id)
            conn.commit()

    # окно обновления вопросов
    def update_question_Ui(self):
        if self.user[4] != None:
            teacher = []
            teacher.append(self.user[4])
            sel_sub = 'SELECT DISTINCT `subjects_id` ' \
                     'FROM `tokens` WHERE `teachers_id` = %s'
            sel_tea = 'SELECT DISTINCT `teachers_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_gr = 'SELECT DISTINCT `groups_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_cour = 'SELECT DISTINCT `courses_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_ye = 'SELECT DISTINCT `year_enter_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_per = 'SELECT DISTINCT `periods_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_bl = 'SELECT DISTINCT `blocks_id` FROM `tokens` ' \
                     'WHERE `teachers_id` = %s'
            cursor.execute(sel_sub, teacher)
            sub = cursor.fetchall()
            cursor.execute(sel_tea, teacher)
            tea = cursor.fetchall()
            cursor.execute(sel_gr, teacher)
            gr = cursor.fetchall()
            cursor.execute(sel_cour, teacher)
            cour = cursor.fetchall()
            cursor.execute(sel_ye, teacher)
            ye = cursor.fetchall()
            cursor.execute(sel_per, teacher)
            per = cursor.fetchall()
            cursor.execute(sel_bl, teacher)
            bl = cursor.fetchall()
            self.combo40 = QComboBox(self)
            for i in range(0, len(sub)):
                sub_id = []
                sub_id.append(int(sub[i][0]))
                sel_sub_name = 'SELECT `name` FROM `subjects` WHERE `id` = %s'
                cursor.execute(sel_sub_name, sub_id)
                self.combo40.addItem(cursor.fetchone()[0])
            self.combo41 = QComboBox(self)
            for i in range(0, len(tea)):
                tea_id = []
                tea_id.append(int(tea[i][0]))
                sel_tea_name = 'SELECT `name` FROM `teachers` WHERE `id` = %s'
                cursor.execute(sel_tea_name, tea_id)
                self.combo41.addItem(cursor.fetchone()[0])
            self.combo42 = QComboBox(self)
            for i in range(0, len(gr)):
                gr_id = []
                gr_id.append(int(gr[i][0]))
                sel_gr_name = 'SELECT `name` FROM `groups` WHERE `id` = %s'
                cursor.execute(sel_gr_name, gr_id)
                self.combo42.addItem(cursor.fetchone()[0])
            self.combo43 = QComboBox(self)
            for i in range(0, len(cour)):
                cour_id = []
                cour_id.append(int(cour[i][0]))
                sel_cour_name = 'SELECT `name` FROM `courses` WHERE `id` = %s'
                cursor.execute(sel_cour_name, cour_id)
                self.combo43.addItem(cursor.fetchone()[0])
            self.combo44 = QComboBox(self)
            for i in range(0, len(ye)):
                ye_id = []
                ye_id.append(int(ye[i][0]))
                sel_ye_name = 'SELECT `name` FROM `year_enter` WHERE `id` = %s'
                cursor.execute(sel_ye_name, ye_id)
                self.combo44.addItem(cursor.fetchone()[0])
            self.combo45 = QComboBox(self)
            for i in range(0, len(per)):
                per_id = []
                per_id.append(int(per[i][0]))
                sel_per_name = 'SELECT `name` FROM `periods` WHERE `id` = %s'
                cursor.execute(sel_per_name, per_id)
                self.combo45.addItem(cursor.fetchone()[0])
            self.combo46 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `type_tasks`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo46.addItem(check_sel[i][0])
            self.combo47 = QComboBox(self)
            for i in range(0, len(bl)):
                bl_id = []
                bl_id.append(int(bl[i][0]))
                sel_bl_name = 'SELECT `name` FROM `blocks` WHERE `id` = %s'
                cursor.execute(sel_bl_name, bl_id)
                self.combo47.addItem(cursor.fetchone()[0])
        else:
            self.combo40 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `subjects`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo40.addItem(check_sel[i][0])
            self.combo41 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `teachers`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo41.addItem(check_sel[i][0])
            self.combo42 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `groups`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo42.addItem(check_sel[i][0])
            self.combo43 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `courses`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo43.addItem(check_sel[i][0])
            self.combo44 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `year_enter`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo44.addItem(check_sel[i][0])
            self.combo45 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `periods`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo45.addItem(check_sel[i][0])
            self.combo46 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `type_tasks`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo46.addItem(check_sel[i][0])
            self.combo47 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `blocks`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo47.addItem(check_sel[i][0])
        hlayout = QHBoxLayout(self)
        self.tabWidget = QTabWidget(self.centralwidget)
        hlayout.addWidget(self.label_31)
        vlayout = QVBoxLayout(self)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.combo40)
        vlayout1 = QVBoxLayout(self)
        vlayout1.addLayout(vlayout)
        vlayout1.addWidget(self.label_32)
        vlayout2 = QVBoxLayout(self)
        vlayout2.addLayout(vlayout1)
        vlayout2.addWidget(self.combo41)
        vlayout3 = QVBoxLayout(self)
        vlayout3.addLayout(vlayout2)
        vlayout3.addWidget(self.label_33)
        vlayout4 = QVBoxLayout(self)
        vlayout4.addLayout(vlayout3)
        vlayout4.addWidget(self.combo42)
        vlayout5 = QVBoxLayout(self)
        vlayout5.addLayout(vlayout4)
        vlayout5.addWidget(self.label_34)
        vlayout6 = QVBoxLayout(self)
        vlayout6.addLayout(vlayout5)
        vlayout6.addWidget(self.combo43)
        vlayout7 = QVBoxLayout(self)
        vlayout7.addLayout(vlayout6)
        vlayout7.addWidget(self.label_35)
        vlayout8 = QVBoxLayout(self)
        vlayout8.addLayout(vlayout7)
        vlayout8.addWidget(self.combo44)
        vlayout9 = QVBoxLayout(self)
        vlayout9.addLayout(vlayout8)
        vlayout9.addWidget(self.label_36)
        vlayout10 = QVBoxLayout(self)
        vlayout10.addLayout(vlayout9)
        vlayout10.addWidget(self.combo45)
        vlayout11 = QVBoxLayout(self)
        vlayout11.addLayout(vlayout10)
        vlayout11.addWidget(self.label_37)
        vlayout12 = QVBoxLayout(self)
        vlayout12.addLayout(vlayout11)
        vlayout12.addWidget(self.combo46)
        vlayout13 = QVBoxLayout(self)
        vlayout13.addLayout(vlayout12)
        vlayout13.addWidget(self.label_38)
        vlayout14 = QVBoxLayout(self)
        vlayout14.addLayout(vlayout13)
        vlayout14.addWidget(self.combo47)
        vlayout15 = QVBoxLayout(self)
        vlayout15.addLayout(vlayout14)
        vlayout15.addWidget(self.update_t)
        self.tabWidget.setTabText(4, "UpdateQ")
        self.update_question_.setLayout(vlayout15)

    # открыть класс с обновлением вопросов
    def update_question(self):
        tokens = []
        tokens.append(self.combo40.currentText())
        tokens.append(self.combo41.currentText())
        tokens.append(self.combo42.currentText())
        tokens.append(self.combo43.currentText())
        tokens.append(self.combo44.currentText())
        tokens.append(self.combo45.currentText())
        tokens.append(self.combo46.currentText())
        tokens.append(self.combo47.currentText())
        self.UT = UpdateQuestion(tokens, self.user)
        self.UT.show()

    # окно удаления вопросов
    def delete_question_Ui(self):
        if self.user[4] != None:
            teacher = []
            teacher.append(self.user[4])
            sel_sub = 'SELECT DISTINCT `subjects_id` ' \
                     'FROM `tokens` WHERE `teachers_id` = %s'
            sel_tea = 'SELECT DISTINCT `teachers_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_gr = 'SELECT DISTINCT `groups_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_cour = 'SELECT DISTINCT `courses_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_ye = 'SELECT DISTINCT `year_enter_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_per = 'SELECT DISTINCT `periods_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_bl = 'SELECT DISTINCT `blocks_id` FROM `tokens` ' \
                     'WHERE `teachers_id` = %s'
            cursor.execute(sel_sub, teacher)
            sub = cursor.fetchall()
            cursor.execute(sel_tea, teacher)
            tea = cursor.fetchall()
            cursor.execute(sel_gr, teacher)
            gr = cursor.fetchall()
            cursor.execute(sel_cour, teacher)
            cour = cursor.fetchall()
            cursor.execute(sel_ye, teacher)
            ye = cursor.fetchall()
            cursor.execute(sel_per, teacher)
            per = cursor.fetchall()
            cursor.execute(sel_bl, teacher)
            bl = cursor.fetchall()
            self.combo50 = QComboBox(self)
            for i in range(0, len(sub)):
                sub_id = []
                sub_id.append(int(sub[i][0]))
                sel_sub_name = 'SELECT `name` FROM `subjects` WHERE `id` = %s'
                cursor.execute(sel_sub_name, sub_id)
                self.combo50.addItem(cursor.fetchone()[0])
            self.combo51 = QComboBox(self)
            for i in range(0, len(tea)):
                tea_id = []
                tea_id.append(int(tea[i][0]))
                sel_tea_name = 'SELECT `name` FROM `teachers` WHERE `id` = %s'
                cursor.execute(sel_tea_name, tea_id)
                self.combo51.addItem(cursor.fetchone()[0])
            self.combo52 = QComboBox(self)
            for i in range(0, len(gr)):
                gr_id = []
                gr_id.append(int(gr[i][0]))
                sel_gr_name = 'SELECT `name` FROM `groups` WHERE `id` = %s'
                cursor.execute(sel_gr_name, gr_id)
                self.combo52.addItem(cursor.fetchone()[0])
            self.combo53 = QComboBox(self)
            for i in range(0, len(cour)):
                cour_id = []
                cour_id.append(int(cour[i][0]))
                sel_cour_name = 'SELECT `name` FROM `courses` WHERE `id` = %s'
                cursor.execute(sel_cour_name, cour_id)
                self.combo53.addItem(cursor.fetchone()[0])
            self.combo54 = QComboBox(self)
            for i in range(0, len(ye)):
                ye_id = []
                ye_id.append(int(ye[i][0]))
                sel_ye_name = 'SELECT `name` FROM `year_enter` WHERE `id` = %s'
                cursor.execute(sel_ye_name, ye_id)
                self.combo54.addItem(cursor.fetchone()[0])
            self.combo55 = QComboBox(self)
            for i in range(0, len(per)):
                per_id = []
                per_id.append(int(per[i][0]))
                sel_per_name = 'SELECT `name` FROM `periods` WHERE `id` = %s'
                cursor.execute(sel_per_name, per_id)
                self.combo55.addItem(cursor.fetchone()[0])
            self.combo56 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `type_tasks`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo56.addItem(check_sel[i][0])
            self.combo57 = QComboBox(self)
            for i in range(0, len(bl)):
                bl_id = []
                bl_id.append(int(bl[i][0]))
                sel_bl_name = 'SELECT `name` FROM `blocks` WHERE `id` = %s'
                cursor.execute(sel_bl_name, bl_id)
                self.combo57.addItem(cursor.fetchone()[0])
        else:
            self.combo50 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `subjects`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo50.addItem(check_sel[i][0])
            self.combo51 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `teachers`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo51.addItem(check_sel[i][0])
            self.combo52 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `groups`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo52.addItem(check_sel[i][0])
            self.combo53 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `courses`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo53.addItem(check_sel[i][0])
            self.combo54 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `year_enter`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo54.addItem(check_sel[i][0])
            self.combo55 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `periods`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo55.addItem(check_sel[i][0])
            self.combo56 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `type_tasks`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo56.addItem(check_sel[i][0])
            self.combo57 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `blocks`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo57.addItem(check_sel[i][0])
        hlayout = QHBoxLayout(self)
        self.tabWidget = QTabWidget(self.centralwidget)
        hlayout.addWidget(self.label_41)
        vlayout = QVBoxLayout(self)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.combo50)
        vlayout1 = QVBoxLayout(self)
        vlayout1.addLayout(vlayout)
        vlayout1.addWidget(self.label_42)
        vlayout2 = QVBoxLayout(self)
        vlayout2.addLayout(vlayout1)
        vlayout2.addWidget(self.combo51)
        vlayout3 = QVBoxLayout(self)
        vlayout3.addLayout(vlayout2)
        vlayout3.addWidget(self.label_43)
        vlayout4 = QVBoxLayout(self)
        vlayout4.addLayout(vlayout3)
        vlayout4.addWidget(self.combo52)
        vlayout5 = QVBoxLayout(self)
        vlayout5.addLayout(vlayout4)
        vlayout5.addWidget(self.label_44)
        vlayout6 = QVBoxLayout(self)
        vlayout6.addLayout(vlayout5)
        vlayout6.addWidget(self.combo53)
        vlayout7 = QVBoxLayout(self)
        vlayout7.addLayout(vlayout6)
        vlayout7.addWidget(self.label_45)
        vlayout8 = QVBoxLayout(self)
        vlayout8.addLayout(vlayout7)
        vlayout8.addWidget(self.combo54)
        vlayout9 = QVBoxLayout(self)
        vlayout9.addLayout(vlayout8)
        vlayout9.addWidget(self.label_46)
        vlayout10 = QVBoxLayout(self)
        vlayout10.addLayout(vlayout9)
        vlayout10.addWidget(self.combo55)
        vlayout11 = QVBoxLayout(self)
        vlayout11.addLayout(vlayout10)
        vlayout11.addWidget(self.label_47)
        vlayout12 = QVBoxLayout(self)
        vlayout12.addLayout(vlayout11)
        vlayout12.addWidget(self.combo56)
        vlayout13 = QVBoxLayout(self)
        vlayout13.addLayout(vlayout12)
        vlayout13.addWidget(self.label_48)
        vlayout14 = QVBoxLayout(self)
        vlayout14.addLayout(vlayout13)
        vlayout14.addWidget(self.combo57)
        vlayout15 = QVBoxLayout(self)
        vlayout15.addLayout(vlayout14)
        vlayout15.addWidget(self.delete_t)
        self.tabWidget.setTabText(5, "DeleteQ")
        self.delete_question_.setLayout(vlayout15)

    # открыть класс с удалением вопросов
    def delete_question(self):
        tokens = []
        tokens.append(self.combo50.currentText())
        tokens.append(self.combo51.currentText())
        tokens.append(self.combo52.currentText())
        tokens.append(self.combo53.currentText())
        tokens.append(self.combo54.currentText())
        tokens.append(self.combo55.currentText())
        tokens.append(self.combo56.currentText())
        tokens.append(self.combo57.currentText())
        self.DT = DeleteQuestion(tokens)
        self.DT.show()

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

    # вывод всех вопросов
    def output_vopr(self):
        all_name = []
        all_name.append(self.combo20.currentText())
        all_name.append(self.combo21.currentText())
        all_name.append(self.combo22.currentText())
        all_name.append(self.combo23.currentText())
        all_name.append(self.combo24.currentText())
        all_name.append(self.combo25.currentText())
        sel_all_id = 'SELECT ' \
                     '(SELECT `id` FROM `subjects` WHERE `name` = %s), ' \
                     '(SELECT `id` FROM `teachers` WHERE `name` = %s), ' \
                     '(SELECT `id` FROM `groups` WHERE `name` = %s), ' \
                     '(SELECT `id` FROM `courses` WHERE `name` = %s), ' \
                     '(SELECT `id` FROM `year_enter` WHERE `name` = %s), ' \
                     '(SELECT `id` FROM `periods` WHERE `name` = %s) ' \
                     'FROM `tokens`'
        cursor.execute(sel_all_id, all_name)
        all_id = cursor.fetchone()
        sel_main_id = 'SELECT `id` FROM `tokens` WHERE `subjects_id` = %s AND `teachers_id` = %s AND `groups_id` = %s ' \
                      'AND `courses_id` = %s AND `year_enter_id` = %s AND `periods_id` = %s'
        cursor.execute(sel_main_id, all_id)
        main_id = cursor.fetchall()
        result = []
        for i in range(0, len(main_id)):
            id_ = []
            sel_id = 'SELECT `subjects_id`, `teachers_id`, `groups_id`, `courses_id`, `year_enter_id`, `periods_id`, ' \
                     '`blocks_id`, `tasks_id`, `type_tasks_id` FROM `tokens` WHERE `id` = %s'
            id_.append(main_id[i][0])
            cursor.execute(sel_id, id_)
            res = cursor.fetchone()
            sel_res = 'SELECT ' \
                          '(SELECT `name` FROM `subjects` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `teachers` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `groups` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `courses` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `year_enter` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `periods` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `blocks` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `tasks` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `type_tasks` WHERE `id` = %s) ' \
                          'FROM `tokens`'
            cursor.execute(sel_res, res)
            result.append(cursor.fetchone())
        doc = aw.Document()
        builder = aw.DocumentBuilder(doc)
        builder.writeln("Дисциплина: " + str(result[0][0]))
        builder.writeln("Преподаватель: " + str(result[0][1]))
        builder.writeln("Группа: " + str(result[0][2]))
        builder.writeln("Курс: " + str(result[0][3]))
        builder.writeln("Год поступления: " + str(result[0][4]))
        builder.writeln("Период: " + str(result[0][5]))
        for g in range(0, len(result)):
            builder.writeln("Тип работы: " + str(result[g][8]))
            builder.writeln("Раздел: " + str(result[g][6]))
            builder.writeln("Задание: " + str(result[g][7]))
        doc.save('Вопросы по дисциплине ' + str(result[0][0]) + '.docx')
        self.label_8.setText('Количество вопросов: ' + str(len(main_id)))

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
        if self.user[4] != None:
            teacher = []
            teacher.append(self.user[4])
            sel_sub = 'SELECT DISTINCT `subjects_id` ' \
                     'FROM `tokens` WHERE `teachers_id` = %s'
            sel_tea = 'SELECT DISTINCT `teachers_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_gr = 'SELECT DISTINCT `groups_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_cour = 'SELECT DISTINCT `courses_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_ye = 'SELECT DISTINCT `year_enter_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_per = 'SELECT DISTINCT `periods_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            cursor.execute(sel_sub, teacher)
            sub = cursor.fetchall()
            cursor.execute(sel_tea, teacher)
            tea = cursor.fetchall()
            cursor.execute(sel_gr, teacher)
            gr = cursor.fetchall()
            cursor.execute(sel_cour, teacher)
            cour = cursor.fetchall()
            cursor.execute(sel_ye, teacher)
            ye = cursor.fetchall()
            cursor.execute(sel_per, teacher)
            per = cursor.fetchall()
            self.combo = QComboBox(self)
            for i in range(0, len(sub)):
                sub_id = []
                sub_id.append(int(sub[i][0]))
                sel_sub_name = 'SELECT `name` FROM `subjects` WHERE `id` = %s'
                cursor.execute(sel_sub_name, sub_id)
                self.combo.addItem(cursor.fetchone()[0])
            self.combo1 = QComboBox(self)
            for i in range(0, len(tea)):
                tea_id = []
                tea_id.append(int(tea[i][0]))
                sel_tea_name = 'SELECT `name` FROM `teachers` WHERE `id` = %s'
                cursor.execute(sel_tea_name, tea_id)
                self.combo1.addItem(cursor.fetchone()[0])
            self.combo2 = QComboBox(self)
            for i in range(0, len(gr)):
                gr_id = []
                gr_id.append(int(gr[i][0]))
                sel_gr_name = 'SELECT `name` FROM `groups` WHERE `id` = %s'
                cursor.execute(sel_gr_name, gr_id)
                self.combo2.addItem(cursor.fetchone()[0])
            self.combo3 = QComboBox(self)
            for i in range(0, len(cour)):
                cour_id = []
                cour_id.append(int(cour[i][0]))
                sel_cour_name = 'SELECT `name` FROM `courses` WHERE `id` = %s'
                cursor.execute(sel_cour_name, cour_id)
                self.combo3.addItem(cursor.fetchone()[0])
            self.combo4 = QComboBox(self)
            for i in range(0, len(ye)):
                ye_id = []
                ye_id.append(int(ye[i][0]))
                sel_ye_name = 'SELECT `name` FROM `year_enter` WHERE `id` = %s'
                cursor.execute(sel_ye_name, ye_id)
                self.combo4.addItem(cursor.fetchone()[0])
            self.combo5 = QComboBox(self)
            for i in range(0, len(per)):
                per_id = []
                per_id.append(int(per[i][0]))
                sel_per_name = 'SELECT `name` FROM `periods` WHERE `id` = %s'
                cursor.execute(sel_per_name, per_id)
                self.combo5.addItem(cursor.fetchone()[0])
        else:
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
        if self.user[4] != None:
            teacher = []
            teacher.append(self.user[4])
            sel_sub = 'SELECT DISTINCT `subjects_id` ' \
                     'FROM `tokens` WHERE `teachers_id` = %s'
            sel_tea = 'SELECT DISTINCT `teachers_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_gr = 'SELECT DISTINCT `groups_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_cour = 'SELECT DISTINCT `courses_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_ye = 'SELECT DISTINCT `year_enter_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            sel_per = 'SELECT DISTINCT `periods_id` ' \
                      'FROM `tokens` WHERE `teachers_id` = %s'
            cursor.execute(sel_sub, teacher)
            sub = cursor.fetchall()
            cursor.execute(sel_tea, teacher)
            tea = cursor.fetchall()
            cursor.execute(sel_gr, teacher)
            gr = cursor.fetchall()
            cursor.execute(sel_cour, teacher)
            cour = cursor.fetchall()
            cursor.execute(sel_ye, teacher)
            ye = cursor.fetchall()
            cursor.execute(sel_per, teacher)
            per = cursor.fetchall()
            self.combo20 = QComboBox(self)
            for i in range(0, len(sub)):
                sub_id = []
                sub_id.append(int(sub[i][0]))
                sel_sub_name = 'SELECT `name` FROM `subjects` WHERE `id` = %s'
                cursor.execute(sel_sub_name, sub_id)
                self.combo20.addItem(cursor.fetchone()[0])
            self.combo21 = QComboBox(self)
            for i in range(0, len(tea)):
                tea_id = []
                tea_id.append(int(tea[i][0]))
                sel_tea_name = 'SELECT `name` FROM `teachers` WHERE `id` = %s'
                cursor.execute(sel_tea_name, tea_id)
                self.combo21.addItem(cursor.fetchone()[0])
            self.combo22 = QComboBox(self)
            for i in range(0, len(gr)):
                gr_id = []
                gr_id.append(int(gr[i][0]))
                sel_gr_name = 'SELECT `name` FROM `groups` WHERE `id` = %s'
                cursor.execute(sel_gr_name, gr_id)
                self.combo22.addItem(cursor.fetchone()[0])
            self.combo23 = QComboBox(self)
            for i in range(0, len(cour)):
                cour_id = []
                cour_id.append(int(cour[i][0]))
                sel_cour_name = 'SELECT `name` FROM `courses` WHERE `id` = %s'
                cursor.execute(sel_cour_name, cour_id)
                self.combo23.addItem(cursor.fetchone()[0])
            self.combo24 = QComboBox(self)
            for i in range(0, len(ye)):
                ye_id = []
                ye_id.append(int(ye[i][0]))
                sel_ye_name = 'SELECT `name` FROM `year_enter` WHERE `id` = %s'
                cursor.execute(sel_ye_name, ye_id)
                self.combo24.addItem(cursor.fetchone()[0])
            self.combo25 = QComboBox(self)
            for i in range(0, len(per)):
                per_id = []
                per_id.append(int(per[i][0]))
                sel_per_name = 'SELECT `name` FROM `periods` WHERE `id` = %s'
                cursor.execute(sel_per_name, per_id)
                self.combo25.addItem(cursor.fetchone()[0])
        else:
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
        hlayout1 = QHBoxLayout(self)
        hlayout1.addLayout(vlayout10)
        hlayout1.addWidget(self.label_8)
        vlayout11 = QVBoxLayout(self)
        vlayout11.addLayout(hlayout1)
        vlayout11.addWidget(self.output_)
        vlayout12 = QVBoxLayout(self)
        vlayout12.addLayout(vlayout11)
        vlayout12.addWidget(self.output_v)
        self.tabWidget1.setTabText(2, "Output")
        self.output.setLayout(vlayout12)

    # окно удаления билетов
    def delete_tokens_Ui(self):
        role_id = []
        role_id.append(self.user[3])
        sel_role_name = 'SELECT `name` FROM `roles` WHERE `id` = %s'
        cursor.execute(sel_role_name, role_id)
        role_name = cursor.fetchone()[0]
        if role_name != 'Преподаватель':
            self.combo60 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `subjects`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo60.addItem(check_sel[i][0])
            self.combo61 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `teachers`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo61.addItem(check_sel[i][0])
            self.combo62 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `groups`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo62.addItem(check_sel[i][0])
            self.combo63 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `courses`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo63.addItem(check_sel[i][0])
            self.combo64 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `year_enter`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo64.addItem(check_sel[i][0])
            self.combo65 = QComboBox(self)
            cursor.execute('SELECT `name` FROM `periods`')
            check_sel = cursor.fetchall()
            for i in range(0, len(check_sel)):
                self.combo65.addItem(check_sel[i][0])
            hlayout = QHBoxLayout(self)
            self.tabWidget = QTabWidget(self.centralwidget)
            hlayout.addWidget(self.label_51)
            vlayout = QVBoxLayout(self)
            vlayout.addLayout(hlayout)
            vlayout.addWidget(self.combo60)
            vlayout1 = QVBoxLayout(self)
            vlayout1.addLayout(vlayout)
            vlayout1.addWidget(self.label_52)
            vlayout2 = QVBoxLayout(self)
            vlayout2.addLayout(vlayout1)
            vlayout2.addWidget(self.combo61)
            vlayout3 = QVBoxLayout(self)
            vlayout3.addLayout(vlayout2)
            vlayout3.addWidget(self.label_53)
            vlayout4 = QVBoxLayout(self)
            vlayout4.addLayout(vlayout3)
            vlayout4.addWidget(self.combo62)
            vlayout5 = QVBoxLayout(self)
            vlayout5.addLayout(vlayout4)
            vlayout5.addWidget(self.label_54)
            vlayout6 = QVBoxLayout(self)
            vlayout6.addLayout(vlayout5)
            vlayout6.addWidget(self.combo63)
            vlayout7 = QVBoxLayout(self)
            vlayout7.addLayout(vlayout6)
            vlayout7.addWidget(self.label_55)
            vlayout8 = QVBoxLayout(self)
            vlayout8.addLayout(vlayout7)
            vlayout8.addWidget(self.combo64)
            vlayout9 = QVBoxLayout(self)
            vlayout9.addLayout(vlayout8)
            vlayout9.addWidget(self.label_56)
            vlayout10 = QVBoxLayout(self)
            vlayout10.addLayout(vlayout9)
            vlayout10.addWidget(self.combo65)
            vlayout15 = QVBoxLayout(self)
            vlayout15.addLayout(vlayout10)
            vlayout15.addWidget(self.delete_token)
            self.tabWidget.setTabText(7, "DeleteTokens")
            self.delete_tokens_.setLayout(vlayout15)

    # удаление билтеов
    def delete_tokens(self):
        tokens = []
        tokens.append(self.combo60.currentText())
        tokens.append(self.combo61.currentText())
        tokens.append(self.combo62.currentText())
        tokens.append(self.combo63.currentText())
        tokens.append(self.combo64.currentText())
        tokens.append(self.combo65.currentText())
        self.DT = DeleteTokens(tokens)
        self.DT.show()

    # сам парсер
    def pars(self):
        # Чтение excel
        global file_
        file = self.file_
        df = pd.read_excel(io=file, engine='openpyxl', sheet_name='Лист1')

        # Парс excel
        result = []

        # Парс ДИСЦИПЛИН
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

    # админка
    def adminIs_Ui(self):
        role_id = []
        role_id.append(self.user[3])
        sel_role_name = 'SELECT `name` FROM `roles` WHERE `id` = %s'
        cursor.execute(sel_role_name, role_id)
        role_name = cursor.fetchone()[0]
        if role_name == 'Администратор':
            vl = QVBoxLayout(self)
            self.tabWidget = QTabWidget(self.centralwidget)
            vl.addWidget(self.options_db)
            vl.addWidget(self.options_users)
            self.tabWidget.setTabText(6, "Admin")
            self.admin_.setLayout(vl)

    # открыть окно настроек БД
    def optionsDB(self):
        self.ODB = OptionsDB(self)
        self.ODB.show()

    # открыть окно настроек пользователей
    def optionsUsers(self):
        self.OU = OptionsUsers(self)
        self.OU.show()

    # диалоговое окно
    def pars_win(self):
        self.open_pars.hide()
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './', '(*.xls *.xlsx)')
        if fname:
            global file_
            self.filename_2.setText(fname)
            self.file_ += str(fname)

    # вывод билетов
    def gen_out(self):
        text, ok = QInputDialog.getText(self, 'Название учебной организации',
                                        'Название: ')
        if ok:
            self.uch_org_line.setText(str(text))
        text, ok = QInputDialog.getText(self, 'Полное название дисциплины',
                                        'Название: ')
        if ok:
            self.full_name_line.setText(str(text))
        doc = aw.Document()
        builder = aw.DocumentBuilder(doc)

        hyphenation_options = doc.hyphenation_options
        hyphenation_options.auto_hyphenation = True
        hyphenation_options.consecutive_hyphen_limit = 2
        all_name = []
        all_name.append(self.combo20.currentText())
        all_name.append(self.combo21.currentText())
        all_name.append(self.combo22.currentText())
        all_name.append(self.combo23.currentText())
        all_name.append(self.combo24.currentText())
        all_name.append(self.combo25.currentText())
        sel_all_id = 'SELECT ' \
                 '(SELECT `id` FROM `subjects` WHERE `name` = %s), ' \
                 '(SELECT `id` FROM `teachers` WHERE `name` = %s), ' \
                 '(SELECT `id` FROM `groups` WHERE `name` = %s), ' \
                 '(SELECT `id` FROM `courses` WHERE `name` = %s), ' \
                 '(SELECT `id` FROM `year_enter` WHERE `name` = %s), ' \
                 '(SELECT `id` FROM `periods` WHERE `name` = %s) ' \
                 'FROM `tokens`'
        cursor.execute(sel_all_id, all_name)
        all_id = cursor.fetchone()
        sel_main_id = 'SELECT `id` FROM `tokens` WHERE `subjects_id` = %s AND `teachers_id` = %s AND `groups_id` = %s ' \
                  'AND `courses_id` = %s AND `year_enter_id` = %s AND `periods_id` = %s'
        cursor.execute(sel_main_id, all_id)
        main_id = cursor.fetchall()
        num_arr = []
        for i in range(0, len(main_id)):
            id_ = []
            id_.append(main_id[i][0])
            sel_num = 'SELECT `number` FROM `exam_tokens` WHERE `tokens_id` = %s'
            cursor.execute(sel_num, id_)
            num_exam = cursor.fetchall()
            if num_exam != None:
                for k in range(0, len(num_exam)):
                    num = num_exam[k][0]
                    if num not in num_arr:
                        num_arr.append(num)
        sprav_main = []
        for i in range(0, len(main_id)):
            sprav_main.append(main_id[i][0])
        for i in range(0, len(num_arr)):
            sel_id_tokens = 'SELECT `tokens_id` FROM `exam_tokens` WHERE `number` = %s'
            number = []
            number.append(num_arr[i])
            cursor.execute(sel_id_tokens, number)
            id_tokens = cursor.fetchall()
            right_id_tokens = []
            for j in range(0, len(id_tokens)):
                if id_tokens[j][0] in sprav_main:
                    right_id_tokens.append(id_tokens[j][0])
            result = []
            for z in range(0, len(right_id_tokens)):
                sel_vopr = 'SELECT `subjects_id`, `teachers_id`, `groups_id`, `courses_id`, `year_enter_id`, `periods_id`, ' \
                           '`tasks_id`, `type_tasks_id`, `blocks_id` FROM `tokens` WHERE `id` = %s'
                id_vopr = []
                id_vopr.append(right_id_tokens[z])
                cursor.execute(sel_vopr, id_vopr)
                res = cursor.fetchone()
                sel_res = 'SELECT ' \
                          '(SELECT `name` FROM `subjects` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `teachers` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `groups` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `courses` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `year_enter` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `periods` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `tasks` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `type_tasks` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `blocks` WHERE `id` = %s) ' \
                          'FROM `tokens`'
                cursor.execute(sel_res, res)
                result.append(cursor.fetchone())
            font = builder.font
            font.size = 14
            font.name = "Times New Romans"

            par_format = builder.paragraph_format
            par_format.alignment = aw.ParagraphAlignment.CENTER

            builder.writeln(f'{str(self.uch_org_line.text())} \nБилет №{num_arr[i]}\nпо дисциплине "{str(self.full_name_line.text())}"')
            builder.writeln("_____________________________________________________________________")

            par_format = builder.paragraph_format
            par_format.alignment = aw.ParagraphAlignment.LEFT
            builder.list_format.apply_number_default()
            for g in range(0, len(result)):
                builder.writeln(str(result[g][6]))
            builder.list_format.remove_numbers()
            builder.write('\n')
            builder.writeln("Зам. директор по УМР:_________________                        ___________________")
            font = builder.font
            font.size = 10
            font.name = "Times New Romans"
            builder.writeln("                                                                      (подпись)                                                            (фамилия, инициалы)")
            font = builder.font
            font.size = 14
            font.name = "Times New Romans"
            builder.writeln("_____________________________________________________________________")
        doc.save(str(self.full_name_line.text()) + '.docx')
        self.label_8.setText('Документ выгружены!')

    # сам генератор
    def generator(self):
        res = []
        type_t = []
        cursor.execute('SELECT `id`, `name` FROM `subjects`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel) + 1):
            if str(check_sel[i][1]) == str(self.combo.currentText()):
                res.append(check_sel[i][0])
                break
        cursor.execute('SELECT `id`, `name` FROM `teachers`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel) + 1):
            if check_sel[i][1] == self.combo1.currentText():
                res.append(check_sel[i][0])
                break
        cursor.execute('SELECT `id`, `name` FROM `groups`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel) + 1):
            if check_sel[i][1] == self.combo2.currentText():
                res.append(check_sel[i][0])
                break
        cursor.execute('SELECT `id`, `name` FROM `courses`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel) + 1):
            if check_sel[i][1] == self.combo3.currentText():
                res.append(check_sel[i][0])
                break
        cursor.execute('SELECT `id`, `name` FROM `year_enter`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel) + 1):
            if str(check_sel[i][1]) == str(self.combo4.currentText()):
                res.append(check_sel[i][0])
                break
        cursor.execute('SELECT `id`, `name` FROM `periods`')
        check_sel = cursor.fetchall()
        for i in range(0, len(check_sel) + 1):
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
            if int(check_blocks_teor[i]) < (int(self.tokens_line.text()) * int(self.num_blocks_t[i])):
                if set_ < math.ceil(
                        (int(self.tokens_line.text()) * int(self.num_blocks_t[i])) / int(check_blocks_teor[i])):
                    set_ = math.ceil(
                        (int(self.tokens_line.text()) * int(self.num_blocks_t[i])) / int(check_blocks_teor[i]))

        if self.practic == True:
            for i in range(0, len(check_blocks_pract)):
                if int(check_blocks_pract[i]) < (int(self.tokens_line.text()) * int(self.num_blocks_p[i])):
                    if set_ < math.ceil(
                            (int(self.tokens_line.text()) * int(self.num_blocks_p[i])) / int(check_blocks_pract[i])):
                        set_ = math.ceil(
                            (int(self.tokens_line.text()) * int(self.num_blocks_p[i])) / int(check_blocks_pract[i]))
                if minimal < int(check_blocks_teor[i]) + int(check_blocks_pract[i]) / int(self.num_blocks_t[i]) + int(
                        self.num_blocks_p[i]):
                    minimal = int(check_blocks_teor[i]) + int(check_blocks_pract[i]) / int(self.num_blocks_t[i]) + int(
                        self.num_blocks_p[i])
        else:
            for i in range(0, len(check_blocks_teor)):
                if minimal < int(check_blocks_teor[i]) / int(self.num_blocks_t[i]):
                    minimal = int(check_blocks_teor[i]) / int(self.num_blocks_t[i])
        sum_p = sum(self.num_blocks_p)
        sum_t = sum(self.num_blocks_t)
        sum_all = sum_p + sum_t
        if set_ == 0:
            set_ += 1
        arr_tok = [[] for x in range(0, set_)]
        for i in range(0, set_):
            for j in range(0, int(self.tokens_line.text()) // set_):
                if sum_all >= minimal:
                    arr_tok[i].append(minimal)
                    sum_all -= minimal
                else:
                    arr_tok[i].append(sum_all)
        type_t.append(0)
        type_t.append(0)
        num_token = 0
        if len(arr_tok) == 0:
            arr_tok.append(int(self.tokens_line.text()))
        for q in range(0, set_):
            for h in range(0, len(arr_tok[q])):
                num_token += 1
                set_q = []
                set_q.append(q+1)
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
                                                    date1 = df.values.tolist()[w][6]
                                                    break
                        time_format = "%Y-%m-%d"
                        input_exam_tokens = 'INSERT INTO `exam_tokens` (`number`, `tokens_id`, `date_exam`, `set`) ' \
                                            'VALUES (%s, %s, %s, %s)'
                        exam_token = []
                        exam_token.append(num_token)
                        exam_token.append(id_token)
                        exam_token.append(f"{date1:{time_format}}")
                        exam_token.append(q + 1)
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
                                                        date1 = df.values.tolist()[w][6]
                                                        break
                            time_format = "%Y-%m-%d"
                            input_exam_tokens = 'INSERT INTO `exam_tokens` (`number`, `tokens_id`, `date_exam`, `set`) ' \
                                                'VALUES (%s, %s, %s, %s)'
                            exam_token = []
                            exam_token.append(num_token)
                            exam_token.append(id_token)
                            exam_token.append(f"{date1:{time_format}}")
                            exam_token.append(q + 1)
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
    w = Login()
    w.show()
    sys.exit(app.exec_())

# ++++++++++++++++++++++++++++++++++++++++++++++++++
'''
АИС
'''
