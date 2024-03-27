import datetime
import time
import json
import mysql.connector
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
import os.path
import aspose.words as aw

delta = datetime.timedelta(days=1)

name_week_day_arr = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']


while True:
    start_time = datetime.datetime.now()
    t = (datetime.datetime.now(datetime.timezone.utc) + delta)
    end_time = datetime.datetime(int(t.strftime('%Y')), int(t.strftime('%m')), int(t.strftime('%d')), 8, 0, 0)
    res = end_time - start_time
    time.sleep(res.seconds)
    # КОД НА ВЫПОЛНЕНИЕ
    with open('config_path.json', encoding="utf8") as conf:
        config = json.load(conf)

    with open(config[0]['config_db'] + '/config_db.json', encoding="utf8") as save:
        json_db = json.load(save)

    with open('config_base_schedule.json', encoding="utf8") as conf_bs:
        config_base_schedule = json.load(conf_bs)

    with open('config_set_email.json', encoding="utf8") as conf_se:
        config_set_email = json.load(conf_se)

    conn = mysql.connector.connect(user=json_db[0]['login'], password=json_db[0]['password'], host=json_db[0]['host'],
                                   database=json_db[0]['name_db'])
    cursor = conn.cursor(buffered=True)
    result = []
    data_db = []
    data_db.append(name_week_day_arr[start_time.weekday()])
    check_input = 'SELECT `id` FROM `name_day` WHERE `name` = %s'
    cursor.execute(check_input, data_db)
    result.append(cursor.fetchone()[0])
    data_db = []
    data_db.append(start_time.strftime("%Y-%m-%d"))
    check_input = 'SELECT `type_week_id` FROM `date_type_week` WHERE `date_week` = %s'
    cursor.execute(check_input, data_db)
    result.append(cursor.fetchone()[0])
    result.append(config_base_schedule[0]['path_line'])
    check_sc = 'SELECT * FROM `schedule_changes` WHERE `date_changes` = %s'
    cursor.execute(check_sc, data_db)
    schedule_c = cursor.fetchall()
    check_sb = 'SELECT * FROM `schedule` WHERE `name_day_id` = %s AND `type_week_id` = %s AND `sprav_schedule_id` = %s'
    cursor.execute(check_sb, result)
    schedule_b = cursor.fetchall()
    schedule_b_edit = []
    for i in range(0, len(schedule_b)):
        schedule_b_edit.append(list(schedule_b[i]))
    for i in range(0, len(schedule_b_edit)):
        for x in range(0, len(schedule_c)):
            if schedule_c[x][1] == schedule_b_edit[i][3] and schedule_c[x][2] == schedule_b_edit[i][4] and\
                    schedule_c[x][3] == schedule_b_edit[i][5] and schedule_c[x][4] == schedule_b_edit[i][6] and\
                    schedule_c[x][8] == schedule_b_edit[i][9] and schedule_c[x][9] == schedule_b_edit[i][10]:
                schedule_b_edit[i][1] = schedule_c[x][5]
                schedule_b_edit[i][2] = schedule_c[x][6]
    for i in range(0, len(schedule_b_edit)):
        if schedule_b_edit[i][2] == None:
            continue
        A = {1: 1, 2: 3, 3: 5, 4: 7}
        B = {1: 2, 2: 4, 3: 6, 4: 8}
        data_db = []
        data_db.append(schedule_b_edit[i][1])
        data_db.append(schedule_b_edit[i][3])
        data_db.append(schedule_b_edit[i][4])
        data_db.append(schedule_b_edit[i][5])
        id_course = []
        id_course.append(schedule_b_edit[i][4])
        sel_course = 'SELECT `name` FROM courses WHERE `id` = %s'
        cursor.execute(sel_course, id_course)
        if int(start_time.strftime('%m')) >= 9:
            data_db.append(A[int(cursor.fetchone()[0])])
        elif int(start_time.strftime('%m')) < 9:
            data_db.append(B[int(cursor.fetchone()[0])])
        check_lp = 'SELECT `id` FROM `lessons_plan` WHERE `subjects_id` = %s AND `groups_id` = %s AND `courses_id` = ' \
                   '%s AND `year_enter_id` = %s AND `term` = %s '
        cursor.execute(check_lp, data_db)
        result = cursor.fetchall()
        data_db = []
        data_db.append(schedule_b_edit[i][2])
        data_db.append(schedule_b_edit[i][10])
        check_cc = 'SELECT `lessons_plan_id` FROM `completed_classes` WHERE `teachers_id` = %s AND `num_group` = %s'
        cursor.execute(check_cc, data_db)
        cc_t = cursor.fetchall()
        if cc_t != None:
            cc_t_arr = []
            for x in range(0, len(cc_t)):
                cc_t_arr.append(cc_t[x][0])
            for x in range(0, len(result)):
                if result[x][0] not in cc_t_arr:
                    res = result[x][0]
                    break
        else:
            res = result[0][0]
        data_db = []
        data_db.append(res)
        data_db.append(schedule_b_edit[i][2])
        data_db.append(schedule_b_edit[i][10])
        data_db.append(start_time.strftime("%Y-%m-%d"))
        insert_cc = 'INSERT INTO `completed_classes` (`lessons_plan_id`, `teachers_id`, `num_group`, `date_classes`) ' \
                    'VALUES (%s, %s, %s, %s)'
        check_input_cc = 'SELECT * FROM `completed_classes` WHERE `lessons_plan_id` = %s AND `teachers_id` = %s AND ' \
                         '`num_group` = %s AND `date_classes` = %s'
        cursor.execute(check_input_cc, data_db)
        res_check = cursor.fetchone()
        if res_check == None:
            cursor.execute(insert_cc, data_db)
            conn.commit()
        data_db = []
        data_db.append(schedule_b_edit[i][2])
        data_db.append(schedule_b_edit[i][10])
        check_cc = 'SELECT `lessons_plan_id` FROM `completed_classes` WHERE `teachers_id` = %s AND `num_group` = %s'
        cursor.execute(check_cc, data_db)
        cc_t = cursor.fetchall()
        cc_t_arr = []
        count = 0
        for x in range(0, len(cc_t)):
            cc_t_arr.append(cc_t[x][0])
        for x in range(0, len(result)):
            if result[x][0] in cc_t_arr:
                count += 1
            else:
                continue
        if count == len(result) and count != 0:
            data_db = []
            data_db.append(result[0][0])
            sel_id_lp = 'SELECT `subjects_id`, `groups_id`, `courses_id`, `year_enter_id` FROM `lessons_plan` WHERE `id` = %s'
            cursor.execute(sel_id_lp, data_db)
            id_lp = cursor.fetchone()
            sel_name_lp = 'SELECT ' \
                          '(SELECT `name` FROM `subjects` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `groups` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `courses` WHERE `id` = %s), ' \
                          '(SELECT `name` FROM `year_enter` WHERE `id` = %s) FROM `lessons_plan`'
            cursor.execute(sel_name_lp, id_lp)
            name_lp = cursor.fetchone()
            sel_id_cc = 'SELECT `teachers_id`, `num_group` FROM `completed_classes` WHERE `lessons_plan_id` = %s'
            cursor.execute(sel_id_cc, data_db)
            id_cc = cursor.fetchone()
            data_db = []
            data_db.append(id_cc[0])
            sel_name_cc = 'SELECT (SELECT `name` FROM `teachers` WHERE `id` = %s) FROM `completed_classes`'
            cursor.execute(sel_name_cc, data_db)
            name_cc = cursor.fetchone()[0]
            doc = aw.Document()
            builder = aw.DocumentBuilder(doc)
            builder.start_table()
            builder.insert_cell()
            builder.paragraph_format.alignment = aw.ParagraphAlignment.CENTER
            builder.font.size = 12
            builder.font.name = "Arial"
            builder.font.bold = True
            builder.cell_format.width = 200.0
            builder.write("Дисциплина")
            builder.insert_cell()
            builder.write("Преподаватель")
            builder.insert_cell()
            builder.write("Направление подготовки")
            builder.insert_cell()
            builder.write("Группа")
            builder.insert_cell()
            builder.write("Курс")
            builder.insert_cell()
            builder.write("Год поступления")
            builder.end_row()
            builder.paragraph_format.alignment = aw.ParagraphAlignment.CENTER
            builder.font.size = 12
            builder.font.name = "Arial"
            builder.font.bold = False
            builder.insert_cell()
            builder.write(str(name_lp[0]))
            builder.insert_cell()
            builder.write(str(name_cc))
            builder.insert_cell()
            builder.write(str(name_lp[1]))
            builder.insert_cell()
            builder.write(str(id_cc[1]))
            builder.insert_cell()
            builder.write(str(name_lp[2]))
            builder.insert_cell()
            builder.write(str(name_lp[3]))
            builder.end_row()
            builder.end_table()
            builder.write('\n')
            builder.start_table()
            builder.insert_cell()
            builder.paragraph_format.alignment = aw.ParagraphAlignment.CENTER
            builder.font.size = 16
            builder.font.name = "Arial"
            builder.font.bold = True
            builder.cell_format.width = 200.0
            builder.write("Название темы")
            builder.insert_cell()
            builder.cell_format.width = 100.0
            builder.write("Даты")
            builder.end_row()
            builder.paragraph_format.alignment = aw.ParagraphAlignment.CENTER
            builder.font.size = 12
            builder.font.name = "Arial"
            builder.font.bold = False
            for x in range(0, len(result)):
                data_db = []
                data_db.append(result[x][0])
                sel_theme = 'SELECT `theme` FROM `lessons_plan` WHERE `id` = %s'
                cursor.execute(sel_theme, data_db)
                theme_n = cursor.fetchone()[0]
                builder.cell_format.width = 200.0
                builder.insert_cell()
                builder.write(str(theme_n))
                sel_date = 'SELECT `date_classes` FROM `completed_classes` WHERE `lessons_plan_id` = %s'
                cursor.execute(sel_date, data_db)
                date_cc = cursor.fetchone()[0]
                builder.insert_cell()
                builder.cell_format.width = 100.0
                builder.write(str(date_cc))
                builder.end_row()
            builder.end_table()
            doc.save(str(name_lp[0]) + " " + str(name_cc) + " " + str(name_lp[1]) + " " + str(name_lp[2]) + ".docx")
            TO_EMAIL = config_set_email[0]['user']
            PWD = config_set_email[0]['password']
            FROM_EMAIL = config_set_email[0]['login']
            SUBJECT = "Отчёт"
            message = MIMEMultipart()
            message["From"] = FROM_EMAIL
            message["To"] = TO_EMAIL
            message["Subject"] = SUBJECT
            attachment_path = str(name_lp[0]) + " " + str(name_cc) + " " + str(name_lp[1]) + " " + str(name_lp[2]) + ".docx"
            attachment_filename = os.path.basename(attachment_path)
            with open(attachment_path, 'rb') as file:
                attachment = MIMEApplication(file.read(), _subtype='docx')
                attachment.add_header('Content-Disposition', 'attachment', filename=attachment_filename)
            message.attach(attachment)
            server = smtplib.SMTP_SSL('smtp.mail.ru:465')
            server.login(FROM_EMAIL, PWD)
            server.sendmail(FROM_EMAIL, TO_EMAIL, message.as_string())
            server.quit()
        result = []