import pymysql
import csv
from cnx_information import BaseManager
from pymysql.cursors import DictCursor
from datetime import datetime, date
import pandas as pd
import numpy as np
import pprint
import xlrd  # 엑셀파일 읽어올 때
import csv  # csv파일 읽어올 때
import traceback   # error 메세지 적을 때

class Worker(BaseManager):
    def __init__(self):
        self.dbname = 'nas'

    def make_data(self):

        # db 연결
        try:
            cnx_db = self.get_cnx(self.dbname, cursorclass=DictCursor, autocommit=False)
            cur_db = cnx_db.cursor()
            print('SUCCESS DB CONNECT')
        except:
            print(traceback.format_exc())

        # variable_list 만들기
        variable_list = []
        with open('C:/Users/senti/Desktop/Regular_Season_Batter.csv', encoding='UTF8') as csv_file:
            csv_rows = csv.reader(csv_file, delimiter=',')
            linecount = 0
            for row in csv_rows:
                if linecount == 0:
                    variable_list = row
                    linecount += 1

        # for i in range(len(variable_list)):
        #     if variable_list[i] == '2B':
        #         variable_list[i] = 'H_2B'
        #     if variable_list[i] == '3B':
        #         variable_list[i] = 'H_3B'
        variable_list.remove('height/weight')
        variable_list.append('height')
        variable_list.append('weight')
        print(variable_list)

        # insert_data 만들기
        insert_dict = dict()
        replace_variable_list = []
        height=0
        weight=0
        with open('C:/Users/senti/Desktop/Regular_Season_Batter.csv', encoding='UTF8') as csv_file:
            csv_rows = csv.DictReader(csv_file, delimiter=',')
            for row in csv_rows:
                for variable in variable_list:
                    if variable != 'height' and variable != 'weight':
                        if row[variable] == '' and row[variable] =='!':
                            replace_variable_list.append(variable)

                if row['height/weight'] != '' and row['height/weight'] != '-':
                    height = int(row['height/weight'].split("/")[0][:-2])
                    weight = int(row['height/weight'].split("/")[1][:-2])
                    # print(height)
                batter_id = row['batter_id']
                year = row['year']
                team = row['team']
                born_date = "".join(filter(str.isdigit, row['year_born']))
                starting_salary = "".join(filter(str.isdigit, row['starting_salary']))
                position = row['position'].split("(")[0]
                handed = row['position'].split(")")[0][-2:-1]
                if batter_id not in insert_dict:
                    insert_dict[batter_id] = dict()
                if year not in insert_dict[batter_id]:
                    insert_dict[batter_id][year] = dict()
                if team not in insert_dict[batter_id][year]:
                    insert_dict[batter_id][year][team] = dict()

                    for variable in variable_list:
                        if variable != 'height' and variable != 'weight' and variable != 'year_born' and variable != 'starting_salary' and variable != 'position' and variable != '2B' and variable != '3B':
                            if row[variable] == '' or row[variable] == '-':
                                row[variable] = None
                            if variable not in insert_dict[batter_id][year][team]:
                                insert_dict[batter_id][year][team][variable] = None
                            if variable in insert_dict[batter_id][year][team]:
                                insert_dict[batter_id][year][team][variable] = row[variable]
                if 'H_2B' not in insert_dict[batter_id][year][team]:
                    insert_dict[batter_id][year][team]['H_2B'] = None
                if 'H_2B' in insert_dict[batter_id][year][team]:
                    insert_dict[batter_id][year][team]['H_2B'] = row['2B']
                if 'H_3B' not in insert_dict[batter_id][year][team]:
                    insert_dict[batter_id][year][team]['H_3B'] = None
                if 'H_3B' in insert_dict[batter_id][year][team]:
                    insert_dict[batter_id][year][team]['H_3B'] = row['3B']
                if 'born_date' not in insert_dict[batter_id][year][team]:
                    insert_dict[batter_id][year][team]['born_date'] = None
                if 'born_date' in insert_dict[batter_id][year][team]:
                    insert_dict[batter_id][year][team]['born_date'] = born_date
                if 'starting_salary' not in insert_dict[batter_id][year][team]:
                    insert_dict[batter_id][year][team]['starting_salary'] = None
                if 'starting_salary' in insert_dict[batter_id][year][team]:
                    insert_dict[batter_id][year][team]['starting_salary'] = starting_salary
                if 'position' not in insert_dict[batter_id][year][team]:
                    insert_dict[batter_id][year][team]['position'] = None
                if 'position' in insert_dict[batter_id][year][team]:
                    insert_dict[batter_id][year][team]['position'] = position
                if 'handed' not in insert_dict[batter_id][year][team]:
                    insert_dict[batter_id][year][team]['handed'] = None
                if 'handed' in insert_dict[batter_id][year][team]:
                    insert_dict[batter_id][year][team]['handed'] = handed
                if 'height' not in insert_dict[batter_id][year][team]:
                    insert_dict[batter_id][year][team]['height'] = None
                if 'height' in insert_dict[batter_id][year][team]:
                    insert_dict[batter_id][year][team]['height'] = height
                if 'weight' not in insert_dict[batter_id][year][team]:
                    insert_dict[batter_id][year][team]['weight'] = None
                if 'weight' in insert_dict[batter_id][year][team]:
                    insert_dict[batter_id][year][team]['weight'] = weight

        # pprint.pprint(insert_dict)

        create_table_name = "Regular_Season_Batter"
        sql_create = """
        CREATE TABLE IF NOT EXISTS `{}` (
        `batter_id` VARCHAR(11) COLLATE utf8mb4_unicode_ci NOT NULL,
        `batter_name` VARCHAR(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `year` YEAR(4) NOT NULL,
        `team` VARCHAR(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `avg` FLOAT DEFAULT NULL,
        `G` INT(11) DEFAULT NULL,
        `AB` INT(11) DEFAULT NULL,
        `R` INT(11) DEFAULT NULL,
        `H` INT(11) DEFAULT NULL,
        `H_2B` INT(11) DEFAULT NULL,
        `H_3B` INT(11) DEFAULT NULL,
        `HR` INT(11) DEFAULT NULL,
        `TB` INT(11) DEFAULT NULL,
        `RBI` INT(11) DEFAULT NULL,
        `SB` INT(11) DEFAULT NULL,
        `CS` INT(11) DEFAULT NULL,
        `BB` INT(11) DEFAULT NULL,
        `HBP` INT(11) DEFAULT NULL,
        `SO` INT(11) DEFAULT NULL,
        `GDP` INT(11) DEFAULT NULL,
        `SLG` FLOAT DEFAULT NULL,
        `OBP` FLOAT DEFAULT NULL,
        `E` INT(11) DEFAULT NULL,
        `born_date` DATE DEFAULT NULL,
        `position` VARCHAR(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `handed` VARCHAR(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `career` VARCHAR(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `starting_salary` VARCHAR(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `OPS` FLOAT DEFAULT NULL,
        `height` INT(11) DEFAULT NULL,
        `weight` INT(11) DEFAULT NULL
        ) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """.format(create_table_name)

        cur_db.execute(sql_create)
        cnx_db.commit()

        sql_ins = """
        INSERT INTO {} (batter_id, batter_name, year, team, avg, G, AB, R, H, H_2B, H_3B, HR, TB, RBI, SB, CS, BB, HBP, SO, GDP, SLG, OBP, E, born_date, position, handed, career, starting_salary, OPS, height, weight)
        VALUES
        (%(batter_id)s, %(batter_name)s, %(year)s, %(team)s, %(avg)s, %(G)s, %(AB)s, %(R)s, %(H)s, %(H_2B)s, %(H_3B)s, %(HR)s, %(TB)s, %(RBI)s, %(SB)s, %(CS)s, %(BB)s, %(HBP)s, %(SO)s, %(GDP)s, %(SLG)s, %(OBP)s, %(E)s, %(born_date)s, %(position)s, %(handed)s, %(career)s, %(starting_salary)s, %(OPS)s, %(height)s, %(weight)s)
        """.format(create_table_name)

        idata = []
        for batter_id in insert_dict:
            for year in insert_dict[batter_id]:
                for team in insert_dict[batter_id][year]:
                    idata.append(dict(
                        batter_id=batter_id,
                        batter_name=insert_dict[batter_id][year][team]['batter_name'],
                        year=year,
                        team=insert_dict[batter_id][year][team]['team'],
                        avg=insert_dict[batter_id][year][team]['avg'],
                        G=insert_dict[batter_id][year][team]['G'],
                        AB=insert_dict[batter_id][year][team]['AB'],
                        R=insert_dict[batter_id][year][team]['R'],
                        H=insert_dict[batter_id][year][team]['H'],
                        H_2B=insert_dict[batter_id][year][team]['H_2B'],
                        H_3B=insert_dict[batter_id][year][team]['H_3B'],
                        HR=insert_dict[batter_id][year][team]['HR'],
                        TB=insert_dict[batter_id][year][team]['TB'],
                        RBI=insert_dict[batter_id][year][team]['RBI'],
                        SB=insert_dict[batter_id][year][team]['SB'],
                        CS=insert_dict[batter_id][year][team]['CS'],
                        BB=insert_dict[batter_id][year][team]['BB'],
                        HBP=insert_dict[batter_id][year][team]['HBP'],
                        SO=insert_dict[batter_id][year][team]['SO'],
                        GDP=insert_dict[batter_id][year][team]['GDP'],
                        SLG=insert_dict[batter_id][year][team]['SLG'],
                        OBP=insert_dict[batter_id][year][team]['OBP'],
                        E=insert_dict[batter_id][year][team]['E'],
                        born_date=insert_dict[batter_id][year][team]['born_date'],
                        position=insert_dict[batter_id][year][team]['position'],
                        handed=insert_dict[batter_id][year][team]['handed'],
                        career=insert_dict[batter_id][year][team]['career'],
                        starting_salary=insert_dict[batter_id][year][team]['starting_salary'],
                        OPS=insert_dict[batter_id][year][team]['OPS'],
                        height=insert_dict[batter_id][year][team]['height'],
                        weight=insert_dict[batter_id][year][team]['weight']
                    ))

        try:
            cur_db.executemany(sql_ins, idata)
            cnx_db.commit()
        except:
            print(traceback.format_exc())

Worker().make_data()