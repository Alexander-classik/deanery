import datetime
import time
import json
import mysql.connector
import os.path

with open('config_path.json', encoding="utf8") as conf:
    config = json.load(conf)

with open(config[0]['config_db']+'/config_db.json', encoding="utf8") as save:
    json_db = json.load(save)

# Подключение к БД
conn = mysql.connector.connect(user=json_db[0]['login'], password=json_db[0]['password'], host=json_db[0]['host'],
                                   database=json_db[0]['name_db'])
cursor = conn.cursor(buffered=True)

delta = datetime.timedelta(days=1)

name_week_day_arr = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']


while True:
    start_time = datetime.datetime.now()
    t = (datetime.datetime.now(datetime.timezone.utc) + delta)
    end_time = datetime.datetime(int(t.strftime('%Y')), int(t.strftime('%m')), int(t.strftime('%d')), 0, 0, 0)
    res = end_time - start_time
    # time.sleep(res.seconds)
    # КОД НА ВЫПОЛНЕНИЕ
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
    check_sc = 'SELECT * FROM `schedule_changes` WHERE `date_changes` = %s'
    cursor.execute(check_sc, data_db)
    schedule_c = cursor.fetchall()
    check_sb = 'SELECT * FROM `schedule` WHERE `name_day_id` = %s AND `type_week_id` = %s'
    cursor.execute(check_sb, result)
    schedule_b = cursor.fetchall()
    schedule_b_edit = []
    for i in range(0, len(schedule_b)):
        schedule_b_edit.append(list(schedule_b[i]))
    for i in range(0, len(schedule_b_edit)):
        for x in range(0, len(schedule_c)):
            if schedule_c[x][1] == schedule_b_edit[i][3] and schedule_c[x][2] == schedule_b_edit[i][4] and schedule_c[x][3] == schedule_b_edit[i][5] and schedule_c[x][4] == schedule_b_edit[i][6] and schedule_c[x][8] == schedule_b_edit[i][9] and schedule_c[x][9] == schedule_b_edit[i][10]:
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
                    'VALUES (%s, %s, %s, %s) '
        check_input_cc = 'SELECT * FROM `completed_classes` WHERE `lessons_plan_id` = %s AND `teachers_id` = %s AND ' \
                         '`num_group` = %s AND `date_classes` = %s'
        cursor.execute(check_input_cc, data_db)
        res_check = cursor.fetchone()
        if res_check == None:
            cursor.execute(insert_cc, data_db)
            conn.commit()
            result = []
        else:
            result = []
